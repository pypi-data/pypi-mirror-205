from __future__ import annotations

from typing import Iterator, cast

import torch
from torch import Tensor

from infer.postprocess.graph import (
    ChunkData,
    ConcatData,
    PostprocessNode,
    ReshapeData,
    SelectData,
    SliceData,
    TransposeData,
)
from infer.postprocess.handler import HandlerData, register_handler
from infer.postprocess.handlers.utils import rectify_dim


@register_handler("inference::cat", num_outputs=1, concrete=False)
def handle_cat(data: HandlerData) -> Iterator[PostprocessNode] | None:
    node = data.default_node
    node.data.concat = ConcatData(dim=rectify_dim(data.node.i("dim"), len(data.output_shape())))
    yield node


@register_handler("aten::embedding", num_inputs=5, num_outputs=1, implicit_inds=(1,))
def handle_embedding_implicit(data: HandlerData) -> Iterator[PostprocessNode] | None:
    # Embedding can be implemented using `gather` downstream.
    yield data.default_node


@register_handler("aten::embedding", num_inputs=5, num_outputs=1, concrete=True)
def handle_embedding_concrete(data: HandlerData) -> Iterator[PostprocessNode] | None:
    weight, indices, padding_idx, scale_grad, sparse = (data.concrete_values[name] for name in data.input_names)
    data.concrete_values[data.output_name] = torch.embedding(weight, indices, padding_idx, scale_grad, sparse)
    return None


@register_handler("aten::slice", num_inputs=5, num_outputs=1, concrete=True)
def handle_slice_concrete(data: HandlerData) -> Iterator[PostprocessNode] | None:
    tensor, dim, start, end, step = (data.concrete_values[i] for i in data.input_names)
    dim = rectify_dim(dim, cast(Tensor, tensor).dim())
    index = [slice(None)] * dim + [slice(start, end, step)]
    new_tensor = tensor[index]
    data.concrete_values[data.output_name] = new_tensor
    return None


@register_handler("aten::slice", num_inputs=5, num_outputs=1, implicit_inds=(0,))
def handle_slice_implicit(data: HandlerData) -> Iterator[PostprocessNode] | None:
    dim, start, end, step = (data.concrete_values[i] for i in data.input_names[1:])
    input_shape = data.shapes[data.input_names[0]]
    dim = rectify_dim(dim, len(input_shape))
    assert (input_dim := input_shape[dim]) is not None
    start, end = rectify_dim(start, input_dim), rectify_dim(end, input_dim)
    node = data.default_node
    node.data.slice = SliceData(dim=dim, start=start, end=end, step=step)
    yield node


@register_handler("aten::select", num_inputs=3, num_outputs=1, implicit_inds=(0,))
def handle_select_implicit(data: HandlerData) -> Iterator[PostprocessNode] | None:
    dim, index = (data.concrete_values[i] for i in data.input_names[1:])
    input_shape = data.shapes[data.input_names[0]]
    dim = rectify_dim(dim, len(input_shape))
    node = data.default_node
    node.data.select = SelectData(dim=dim, index=index)
    yield node


@register_handler("aten::expand_as", num_inputs=2, num_outputs=1, implicit_inds=(1,))
@register_handler("aten::expand_as", num_inputs=2, num_outputs=1, concrete=True)
def handle_expand_as_implicit(data: HandlerData) -> Iterator[PostprocessNode] | None:
    base_name, ref_name = data.input_names
    tensor = data.concrete_values[base_name]
    data.concrete_values[data.output_name] = tensor.expand(data.shapes[ref_name])
    return None


@register_handler("aten::unflatten", num_outputs=1, implicit_inds=(0,))
@register_handler("aten::flatten", num_outputs=1, implicit_inds=(0,))
@register_handler("aten::squeeze", num_outputs=1, implicit_inds=(0,))
@register_handler("aten::unsqueeze", num_outputs=1, implicit_inds=(0,))
@register_handler("aten::view", num_outputs=1, implicit_inds=(0,))
def handle_view_implicit(data: HandlerData) -> Iterator[PostprocessNode] | None:
    node = data.default_node
    node.data.reshape = ReshapeData(shape=data.output_shape())
    node.op = "aten::reshape"
    yield node


@register_handler("aten::unflatten", num_inputs=4, num_outputs=1, concrete=True)
def handle_unflatten_concrete(data: HandlerData) -> Iterator[PostprocessNode] | None:
    input_tensor, dim, shape, _ = (data.concrete_values[name] for name in data.input_names)
    data.concrete_values[data.output_name] = input_tensor.unflatten(dim, shape)
    return None


@register_handler("aten::unsqueeze", num_inputs=2, num_outputs=1, concrete=True)
def handle_unsqueeze_concrete(data: HandlerData) -> Iterator[PostprocessNode] | None:
    input_tensor, unsqueeze_dim = (data.concrete_values[name] for name in data.input_names)
    data.concrete_values[data.output_name] = input_tensor.unsqueeze(unsqueeze_dim)
    return None


@register_handler("aten::view", num_inputs=2, num_outputs=1, concrete=True)
@register_handler("aten::reshape", num_inputs=2, num_outputs=1, concrete=True)
def handle_view_concrete(data: HandlerData) -> Iterator[PostprocessNode] | None:
    input_tensor, new_shape = (data.concrete_values[name] for name in data.input_names)
    data.concrete_values[data.output_name] = input_tensor.reshape(new_shape)
    return None


@register_handler("aten::transpose", num_inputs=3, num_outputs=1, implicit_inds=(0,))
def handle_transpose(data: HandlerData) -> Iterator[PostprocessNode] | None:
    dim_a, dim_b = (data.concrete_values[name] for name in data.input_names[1:])
    ndim = len(data.input_shape(i=0))
    dim_a, dim_b = rectify_dim(dim_a, ndim), rectify_dim(dim_b, ndim)
    node = data.default_node
    node.data.transpose = TransposeData(dim_a=dim_a, dim_b=dim_b)
    yield node


@register_handler("inference::chunk", num_inputs=1, concrete=False)
def handle_chunk(data: HandlerData) -> Iterator[PostprocessNode] | None:
    node = data.default_node
    dim = rectify_dim(data.node.i("dim"), len(data.input_shape(i=0)))
    node.data.chunk = ChunkData(dim=dim, num_chunks=data.num_outputs)
    yield node
