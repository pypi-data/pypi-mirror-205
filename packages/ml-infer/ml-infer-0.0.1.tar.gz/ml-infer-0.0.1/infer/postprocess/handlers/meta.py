from __future__ import annotations

import re
from typing import Iterator, cast

import torch
from torch import Tensor

from infer.postprocess.graph import PostprocessNode
from infer.postprocess.handler import HandlerData, register_handler


@register_handler("prim::GetAttr", num_inputs=1, num_outputs=1, concrete=True)
def handle_getattr(data: HandlerData) -> Iterator[PostprocessNode] | None:
    data.concrete_values[data.output_name] = getattr(data.concrete_values[data.input_name], data.node.s("name"))
    return None


@register_handler("prim::Constant", num_inputs=0, num_outputs=1, concrete=True)
def handle_constant(data: HandlerData) -> Iterator[PostprocessNode] | None:
    const_type = data.node.output().type().kind()
    if const_type == "IntType":
        data.concrete_values[data.output_name] = data.node.i("value")
    elif const_type == "BoolType":
        data.concrete_values[data.output_name] = bool(data.node.i("value"))
    elif const_type == "FloatType":
        data.concrete_values[data.output_name] = data.node.f("value")
    elif const_type == "StringType":
        data.concrete_values[data.output_name] = data.node.s("value")
    elif const_type in ("DictType", "ListType", "TupleType"):
        # Somewhat hacky way to do this, but the C++ API doesn't expose these.
        match = re.search(r"prim::Constant\[value=(.+?)\]\(\)", str(data.node))
        assert match is not None, "Couldn't parse constant value from node"
        data.concrete_values[data.output_name] = eval(match.group(1))  # pylint: disable=eval-used
    elif const_type == "NoneType":
        data.concrete_values[data.output_name] = None
    else:
        raise NotImplementedError(f"Unexpected {const_type=}")
    return None


@register_handler("aten::size", num_inputs=1, num_outputs=1, concrete=False)
def handle_size(data: HandlerData) -> Iterator[PostprocessNode] | None:
    data.concrete_values[data.output_name] = data.shapes[data.input_name]
    return None


@register_handler("aten::size", num_inputs=2, num_outputs=1, implicit_inds=(0,))
def handle_size_ind(data: HandlerData) -> Iterator[PostprocessNode] | None:
    ind = data.concrete_values[data.input_names[1]]
    data.concrete_values[data.output_name] = data.shapes[data.input_names[0]][ind]
    return None


@register_handler("aten::__getitem__", num_inputs=2, num_outputs=1, concrete=True)
def handle_getitem(data: HandlerData) -> Iterator[PostprocessNode] | None:
    list_val, index_val = (data.concrete_values[i] for i in data.input_names)
    data.concrete_values[data.output_name] = list_val[index_val]
    return None


@register_handler("aten::len", num_inputs=1, num_outputs=1, concrete=True)
def handle_len(data: HandlerData) -> Iterator[PostprocessNode] | None:
    data.concrete_values[data.output_name] = len(data.concrete_values[data.input_name])
    return None


@register_handler("prim::Param", num_inputs=0)
def handle_param(data: HandlerData) -> Iterator[PostprocessNode] | None:
    yield data.default_node


@register_handler("prim::Return", num_outputs=0)
def handle_return(data: HandlerData) -> Iterator[PostprocessNode] | None:
    yield data.default_node


@register_handler("aten::contiguous", num_inputs=2, num_outputs=1, implicit_inds=(0,))
@register_handler("aten::contiguous", num_outputs=1, concrete=False)
def handle_contiguous_implicit(data: HandlerData) -> Iterator[PostprocessNode] | None:
    node = data.default_node
    node.data.delete = True
    yield node


@register_handler("aten::contiguous", num_inputs=2, num_outputs=1, implicit_inds=(1,))
@register_handler("aten::contiguous", num_outputs=1, concrete=True)
def handle_contiguous_concrete(data: HandlerData) -> Iterator[PostprocessNode] | None:
    data.concrete_values[data.output_name] = cast(Tensor, data.concrete_values[data.input_name]).contiguous()
    return None


@register_handler("aten::item", num_inputs=1, num_outputs=1, concrete=False)
def handle_item_implicit(data: HandlerData) -> Iterator[PostprocessNode] | None:
    node = data.default_node
    node.data.delete = True
    yield node


@register_handler("prim::device", num_inputs=1, num_outputs=1)
def handle_device(data: HandlerData) -> Iterator[PostprocessNode] | None:
    data.concrete_values[data.output_name] = torch.device("cpu")
    return None


@register_handler("prim::dtype", num_inputs=1, num_outputs=1)
def handle_dtype(data: HandlerData) -> Iterator[PostprocessNode] | None:
    data.concrete_values[data.output_name] = torch.float64
    return None
