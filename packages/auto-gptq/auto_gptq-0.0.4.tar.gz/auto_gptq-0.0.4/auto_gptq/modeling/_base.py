import json
import os
from dataclasses import dataclass, field, fields
from logging import getLogger
from os.path import join
from typing import Dict, List, Union

import torch
import torch.nn as nn
import transformers
from safetensors.torch import load_file as safe_load, save_file as safe_save
from transformers import AutoConfig, AutoModelForCausalLM, PreTrainedModel

from ._const import *
from ._utils import *
from ..quantization import GPTQ

logger = getLogger(__name__)


@dataclass
class BaseQuantizeConfig:
    bits: int = field(default=4, metadata={"choices": [2, 3, 4, 8]})
    damp_percent: float = field(default=0.01)
    desc_act: bool = field(default=True)
    group_size: int = field(default=-1)

    def __post_init__(self):
        fields_info = fields(self)

        if self.bits not in fields_info[0].metadata["choices"]:
            raise ValueError(f"only support quantize to {fields_info[0].metadata['choices']} bits.")
        if not (0 < self.damp_percent < 1):
            raise ValueError("damp_percent must between 0 and 1.")
        if self.group_size != -1 and self.group_size <= 0:
            raise ValueError("unless equal to -1, group_size must greater then 0.")

    def save_pretrained(self, save_dir: str):
        with open(join(save_dir, "quantize_config.json"), "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def from_pretrained(cls, save_dir: str):
        with open(join(save_dir, "quantize_config.json"), "r", encoding="utf-8") as f:
            return cls(**json.load(f))

    def to_dict(self):
        return {
            "bits": self.bits,
            "damp_percent": self.damp_percent,
            "desc_act": self.desc_act,
            "group_size": self.group_size
        }


class BaseGPTQForCausalLM(nn.Module):
    layers_block_name: str = None
    outside_layer_modules: List[str] = None
    inside_layer_modules: List[List[str]] = None
    lm_head_name: str = "lm_head"

    def __init__(self, model: PreTrainedModel, quantized: bool, quantize_config: BaseQuantizeConfig):
        super().__init__()

        self.model = model
        self.model_type = self.model.config.model_type
        self._quantized = quantized
        self.quantize_config = quantize_config
        self.config = self.model.config

    @property
    def quantized(self):
        return self._quantized

    def _move_outside_layer_modules(self, device):
        for module_name in self.outside_layer_modules:
            module = get_module_by_name(self.model, module_name)
            if module is not None:
                module.to(device)

    @staticmethod
    def _resize_attention_mask(attention_mask: List[torch.LongTensor]):
        return attention_mask

    @staticmethod
    def _resize_position_ids(position_ids: List[torch.LongTensor]):
        return position_ids

    @torch.no_grad()
    def quantize(
        self,
        examples: List[Dict[str, torch.LongTensor]],
        use_triton: bool = False,
        autotune_warmup_after_quantized: bool = False
    ):
        if self.quantized:
            raise EnvironmentError("can't execute quantize because the model is quantized.")

        layer_inputs = []
        attention_masks = []
        position_ids = []
        layer_outputs = []
        layer_input_kwargs = []

        class LayerHijacker(nn.Module):
            """hijack layer's forward pass to cache data"""

            def __init__(self, m):
                super().__init__()
                self.module = m

            def forward(self, inp=None, **kwargs):
                if inp is None:  # some models use all key-value arguments in forward pass call
                    for kwarg_name in ["hidden_states"]:
                        if kwarg_name in kwargs:
                            inp = kwargs[kwarg_name]
                            break
                bsz = inp.size(0)
                for i in range(bsz):
                    layer_inputs.append(inp[i].unsqueeze(0).to(CPU))
                    attention_masks.append(kwargs["attention_mask"][i].to(CPU))
                    if (pos_ids := kwargs.get("position_ids", None)) is not None:
                        position_ids.append(pos_ids[i].unsqueeze(0).to(CPU))
                    one_kwargs = dict()
                    for k, v in kwargs.items():  # make sure other arguments also be captured
                        if k not in ["hidden_states", "attention_mask", "position_ids"]:
                            if isinstance(v, torch.Tensor):
                                one_kwargs[k] = v[i].unsqueeze(0).to(CPU)
                            else:
                                one_kwargs[k] = v
                    layer_input_kwargs.append(one_kwargs)
                raise ValueError

        forward_pass_use_cache = self.model.config.use_cache
        self.model.config.use_cache = False

        num_examples = len(examples)
        layers = get_module_by_name(self.model, self.layers_block_name)

        layers[0] = layers[0].to(CUDA)
        self._move_outside_layer_modules(CUDA)

        # get inputs for first layer
        layers[0] = LayerHijacker(layers[0])
        for example in examples:
            for k, v in example.items():
                if len(v.shape) == 1:
                    v = v.unsqueeze(0)
                example[k] = v.to(CUDA)
            try:
                self.model(**example)
            except ValueError:
                pass
        layers[0] = layers[0].module

        layers[0] = layers[0].cpu()
        self._move_outside_layer_modules(CPU)

        torch.cuda.empty_cache()

        # resize attention mask for some special models
        attention_masks = self._resize_attention_mask(attention_masks)
        position_ids = self._resize_position_ids(position_ids)

        quantizers = {}
        for i in range(len(layers)):
            logger.info(f"Start quantizing layer {i + 1}/{len(layers)}")
            layer = layers[i].to(CUDA)

            full = find_layers(layer)
            for names in self.inside_layer_modules:
                subset = {n: full[n] for n in names}
                gptq = {}
                for name in subset:
                    gptq[name] = GPTQ(subset[name])
                    gptq[name].quantizer.configure(
                        self.quantize_config.bits,
                        perchannel=True,
                        sym=True,
                        mse=False
                    )

                def add_batch(name):
                    def tmp(_, inp, out):
                        gptq[name].add_batch(inp[0].data, out.data)

                    return tmp

                handles = []
                for name in subset:
                    handles.append(subset[name].register_forward_hook(add_batch(name)))
                for j in range(num_examples):
                    layer_input = layer_inputs[j].to(CUDA)
                    layer_attention_mask = attention_masks[j].to(CUDA)
                    additional_layer_inputs = {
                        "attention_mask": layer_attention_mask
                    }
                    if (layer_position_ids := None if not position_ids else position_ids[j].to(CUDA)) is not None:
                        additional_layer_inputs["position_ids"] = layer_position_ids
                    for k, v in layer_input_kwargs[j].items():
                        if isinstance(v, torch.Tensor):
                            additional_layer_inputs[k] = v.to(CUDA)
                        else:
                            additional_layer_inputs[k] = v
                    layer(layer_input, **additional_layer_inputs)[0][0].cpu()
                for h in handles:
                    h.remove()

                for name in subset:
                    logger.info(f'Quantizing {name} in layer {i + 1}/{len(layers)}...')
                    scale, zero, g_idx = gptq[name].fasterquant(
                        percdamp=self.quantize_config.damp_percent,
                        groupsize=self.quantize_config.group_size,
                        actorder=self.quantize_config.desc_act
                    )
                    quantizers[f'{self.layers_block_name}.{i}.{name}'] = (
                        gptq[name].quantizer.cpu(), scale.cpu(), zero.cpu(), g_idx.cpu()
                    )
                    gptq[name].free()

            for j in range(num_examples):
                layer_input = layer_inputs[j].to(CUDA)
                layer_attention_mask = attention_masks[j].to(CUDA)
                additional_layer_inputs = {
                    "attention_mask": layer_attention_mask
                }
                if (layer_position_ids := None if not position_ids else position_ids[j].to(CUDA)) is not None:
                    additional_layer_inputs["position_ids"] = layer_position_ids
                for k, v in layer_input_kwargs[j].items():
                    if isinstance(v, torch.Tensor):
                        additional_layer_inputs[k] = v.to(CUDA)
                    else:
                        additional_layer_inputs[k] = v
                layer_output = layer(layer_input, **additional_layer_inputs)[0][0].cpu()
                layer_outputs.append(layer_output.unsqueeze(0))

            layers[i] = layer.to(CPU)
            del layer
            del gptq
            torch.cuda.empty_cache()

            layer_inputs, layer_outputs = layer_outputs, []

        pack_model(
            model=self.model,
            quantizers=quantizers,
            bits=self.quantize_config.bits,
            group_size=self.quantize_config.group_size,
            use_triton=use_triton,
            autotune_warmup=autotune_warmup_after_quantized
        )
        self._quantized = True
        self.model.config.use_cache = forward_pass_use_cache

    @property
    def device(self):
        return self.model.device

    def to(self, device: Union[str, torch.device]):
        self.model.to(device)

    def forward(self, **kwargs):
        return self.model(**kwargs)

    def generate(self, **kwargs):
        """shortcut for model.generate"""
        with torch.inference_mode(), torch.amp.autocast(device_type=self.device.type):
            return self.model.generate(**kwargs)

    def prepare_inputs_for_generation(self, *args, **kwargs):
        """shortcut for model.prepare_inputs_for_generation"""
        return self.model.prepare_inputs_for_generation(*args, **kwargs)

    def save_quantized(self, save_dir: str, use_safetensors: bool = False):
        """save quantized model and configs to local disk"""
        os.makedirs(save_dir, exist_ok=True)

        if not self.quantized:
            raise EnvironmentError("can only save quantized model, please execute .quantize first.")

        self.model.to(CPU)

        model_save_name = f"gptq_model-{self.quantize_config.bits}bit"
        if use_safetensors:
            model_save_name += ".safetensors"
            state_dict = self.model.state_dict()
            state_dict = {k: v.clone().contiguous() for k, v in state_dict.items()}
            safe_save(state_dict, join(save_dir, model_save_name))
        else:
            model_save_name += ".bin"
            torch.save(self.model.state_dict(), join(save_dir, model_save_name))

        self.model.config.save_pretrained(save_dir)
        self.quantize_config.save_pretrained(save_dir)

    @classmethod
    def from_pretrained(
        cls,
        pretrained_model_name_or_path: str,
        quantize_config: BaseQuantizeConfig,
        bf16: bool = False,
        **model_init_kwargs
    ):
        """load un-quantized pretrained model to cpu"""

        def skip(*args, **kwargs):
            pass

        torch.nn.init.kaiming_uniform_ = skip
        torch.nn.init.uniform_ = skip
        torch.nn.init.normal_ = skip

        config = AutoConfig.from_pretrained(pretrained_model_name_or_path, trust_remote_code=True)
        if config.model_type not in SUPPORTED_MODELS:
            raise TypeError(f"{config.model_type} isn't supported yet.")

        # enforce some values despite user specified
        model_init_kwargs["device_map"] = None
        model_init_kwargs["torch_dtype"] = torch.bfloat16 if bf16 else torch.float16
        model_init_kwargs["low_cpu_mem_usage"] = False
        model_init_kwargs["trust_remote_code"] = True

        model = AutoModelForCausalLM.from_pretrained(pretrained_model_name_or_path, **model_init_kwargs)
        model_config = model.config.to_dict()
        seq_len_keys = ["max_position_embeddings", "seq_length"]
        if any([k in model_config for k in seq_len_keys]):
            for key in seq_len_keys:
                if key in model_config:
                    model.seqlen = model_config[key]
                    break
        else:
            logger.warning("can't get model's sequence length from model config, will set to 4096.")
            model.seqlen = 4096
        model.eval()

        return cls(model, False, quantize_config)

    @classmethod
    def from_quantized(
        cls,
        save_dir: str,
        device: str = "cpu",
        use_safetensors: bool = False,
        use_triton: bool = False
    ):
        """load quantized model from local disk"""
        if use_triton:
            from ..nn_modules.qlinear_triton import autotune_warmup_linear

            logger.warning("use_triton will force moving the hole model to GPU, make sure you have enough VRAM.")
            device = "cuda:0"

        config = AutoConfig.from_pretrained(save_dir, trust_remote_code=True)
        if config.model_type not in SUPPORTED_MODELS:
            raise TypeError(f"{config.model_type} isn't supported yet.")

        quantize_config = BaseQuantizeConfig.from_pretrained(save_dir)

        model_save_name = join(save_dir, f"gptq_model-{quantize_config.bits}bit")
        if use_safetensors:
            model_save_name += ".safetensors"
        else:
            model_save_name += ".bin"

        def skip(*args, **kwargs):
            pass

        torch.nn.init.kaiming_uniform_ = skip
        torch.nn.init.uniform_ = skip
        torch.nn.init.normal_ = skip

        transformers.modeling_utils._init_weights = False
        torch.set_default_dtype(torch.half)
        model = AutoModelForCausalLM.from_config(config, trust_remote_code=True)
        torch.set_default_dtype(torch.float)
        model = model.eval()
        layers = find_layers(model)
        for name in [cls.lm_head_name]:
            if name in layers:
                del layers[name]
        make_quant(model, layers, quantize_config.bits, quantize_config.group_size, use_triton=use_triton)

        if model_save_name.endswith('.safetensors'):
            model.load_state_dict(safe_load(model_save_name, "cpu"))
        else:
            model.load_state_dict(torch.load(model_save_name))
        model_config = model.config.to_dict()
        seq_len_keys = ["max_position_embeddings", "seq_length"]
        if any([k in model_config for k in seq_len_keys]):
            for key in seq_len_keys:
                if key in model_config:
                    model.seqlen = model_config[key]
                    break
        else:
            logger.warning("can't get model's sequence length from model config, will set to 4096.")
            model.seqlen = 4096

        model.eval()
        model.to(device)

        if use_triton:
            autotune_warmup_linear(model, seqlen=model.seqlen)

        return cls(model, True, quantize_config)


__all__ = ["BaseGPTQForCausalLM", "BaseQuantizeConfig"]
