from __future__ import annotations

from typing import Iterator

from infer.postprocess.graph import ArgmaxData, ClampData, PostprocessNode, SoftmaxData
from infer.postprocess.handler import HandlerData, register_handler
from infer.postprocess.handlers.utils import rectify_dim


@register_handler("aten::hardtanh", num_inputs=3, num_outputs=1, implicit_inds=(0,))
@register_handler("aten::hardtanh_", num_inputs=3, num_outputs=1, implicit_inds=(0,))
@register_handler("aten::clamp", num_inputs=3, num_outputs=1, implicit_inds=(0,))
@register_handler("aten::clamp_", num_inputs=3, num_outputs=1, implicit_inds=(0,))
def handle_hardtanh(data: HandlerData) -> Iterator[PostprocessNode] | None:
    min_val, max_val = (data.concrete_values[name] for name in data.input_names[1:])
    node = data.default_node
    node.op = "aten::clamp"
    node.data.clamp = ClampData(min_val=min_val, max_val=max_val)
    yield node


@register_handler("aten::relu", num_inputs=1, num_outputs=1, implicit_inds=(0,))
@register_handler("aten::relu_", num_inputs=1, num_outputs=1, implicit_inds=(0,))
def handle_relu(data: HandlerData) -> Iterator[PostprocessNode] | None:
    node = data.default_node
    node.op = "aten::clamp"
    node.data.clamp = ClampData(min_val=0.0, max_val=None)
    yield node


@register_handler("aten::clamp_min", num_inputs=2, num_outputs=1, implicit_inds=(0,))
@register_handler("aten::clamp_min_", num_inputs=2, num_outputs=1, implicit_inds=(0,))
def handle_clamp_min(data: HandlerData) -> Iterator[PostprocessNode] | None:
    min_val = data.concrete_values[data.input_names[1]]
    node = data.default_node
    node.op = "aten::clamp"
    node.data.clamp = ClampData(min_val=min_val, max_val=None)
    yield node


@register_handler("aten::clamp_max", num_inputs=2, num_outputs=1, implicit_inds=(0,))
@register_handler("aten::clamp_max_", num_inputs=2, num_outputs=1, implicit_inds=(0,))
def handle_clamp_max(data: HandlerData) -> Iterator[PostprocessNode] | None:
    max_val = data.concrete_values[data.input_names[1]]
    node = data.default_node
    node.op = "aten::clamp"
    node.data.clamp = ClampData(min_val=None, max_val=max_val)
    yield node


@register_handler("aten::softmax", num_inputs=3, num_outputs=1, implicit_inds=(0,))
def handle_softmax(data: HandlerData) -> Iterator[PostprocessNode] | None:
    dim, dtype = (data.concrete_values[name] for name in data.input_names[1:])
    assert dtype is None
    dim = rectify_dim(dim, len(data.output_shape(i=0)))
    node = data.default_node
    node.data.softmax = SoftmaxData(dim)
    yield node


@register_handler("aten::argmax", num_inputs=3, num_outputs=1, implicit_inds=(0,))
def handle_argmax(data: HandlerData) -> Iterator[PostprocessNode] | None:
    dim, keep_dim = (data.concrete_values[name] for name in data.input_names[1:])
    dim = rectify_dim(dim, len(data.output_shape(i=0)))
    node = data.default_node
    node.data.argmax = ArgmaxData(dim=dim, keep_dim=keep_dim)
    yield node


@register_handler("aten::sigmoid", num_inputs=1, num_outputs=1, concrete=False)
def handle_sigmoid(data: HandlerData) -> Iterator[PostprocessNode] | None:
    yield data.default_node
