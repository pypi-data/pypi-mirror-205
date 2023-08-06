from __future__ import annotations

from typing import Iterator

from infer.postprocess.graph import PostprocessNode, ReduceMeanData, ReduceSumData
from infer.postprocess.handler import HandlerData, register_handler
from infer.postprocess.handlers.utils import rectify_dim


@register_handler("aten::sum", num_inputs=4, num_outputs=1, implicit_inds=(0,))
def handle_sum(data: HandlerData) -> Iterator[PostprocessNode] | None:
    dims, keep_dim, dtype = (data.concrete_values[name] for name in data.input_names[1:])
    assert dtype is None
    dims = tuple(rectify_dim(dim, len(data.input_shape(i=0))) for dim in dims)
    node = data.default_node
    node.data.reduce_sum = ReduceSumData(dims=dims, keep_dim=keep_dim)
    yield node


@register_handler("aten::mean", num_inputs=4, num_outputs=1, implicit_inds=(0,))
def handle_mean(data: HandlerData) -> Iterator[PostprocessNode] | None:
    dims, keep_dim, dtype = (data.concrete_values[name] for name in data.input_names[1:])
    assert dtype is None
    dims = tuple(rectify_dim(dim, len(data.input_shape(i=0))) for dim in dims)
    node = data.default_node
    node.data.reduce_mean = ReduceMeanData(dims=dims, keep_dim=keep_dim)
    yield node
