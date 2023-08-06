from __future__ import annotations

from typing import Iterator, Tuple, cast

import torch

from infer.postprocess.graph import LayerNormData, PostprocessNode
from infer.postprocess.handler import HandlerData, register_handler


@register_handler("aten::layer_norm", num_inputs=6, num_outputs=1, implicit_inds=(0,))
def handle_layer_norm(data: HandlerData) -> Iterator[PostprocessNode] | None:
    shape, weight, bias, eps, _ = (data.concrete_values[name] for name in data.input_names[1:])
    node = data.default_node
    node.data.layer_norm = LayerNormData(shape=cast(Tuple[int, ...], tuple(shape)), weight=weight, bias=bias, eps=eps)
    yield node


@register_handler("aten::layer_norm", num_inputs=6, num_outputs=1, concrete=True)
def handle_layer_norm_concrete(data: HandlerData) -> Iterator[PostprocessNode] | None:
    input_tensor, shape, weight, bias, eps, cudnn_enabled = (data.concrete_values[name] for name in data.input_names)
    data.concrete_values[data.output_name] = torch.layer_norm(input_tensor, shape, weight, bias, eps, cudnn_enabled)
    return None
