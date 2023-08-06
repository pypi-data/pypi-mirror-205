from __future__ import annotations

from typing import Iterator

from infer.postprocess.graph import PostprocessNode
from infer.postprocess.handler import HandlerData, register_handler


@register_handler("prim::ListUnpack", num_inputs=1, concrete=True)
def handle_list_unpack(data: HandlerData) -> Iterator[PostprocessNode] | None:
    list_vals = data.concrete_values[data.input_name]
    assert len(list_vals) == len(data.output_names)
    for list_val, output_name in zip(list_vals, data.output_names):
        data.concrete_values[output_name] = list_val
    return None


@register_handler("prim::ListConstruct", num_outputs=1, concrete=True)
def handle_list_construct_concrete(data: HandlerData) -> Iterator[PostprocessNode] | None:
    new_list = [data.concrete_values[i.debugName()] for i in data.node.inputs()]
    data.concrete_values[data.node.output().debugName()] = new_list
    return None


@register_handler("prim::ListConstruct", num_outputs=1, concrete=False)
def handle_list_construct(data: HandlerData) -> Iterator[PostprocessNode] | None:
    node = data.default_node
    node.data.delete = True
    yield node


@register_handler("prim::DictConstruct", num_outputs=1, concrete=True)
def handle_dict_construct_concrete(data: HandlerData) -> Iterator[PostprocessNode] | None:
    inputs, output = list(data.node.inputs()), data.node.outputsAt(0)
    new_dict = {
        data.concrete_values[inputs[i].debugName()]: data.concrete_values[inputs[i + 1].debugName()]
        for i in range(0, len(inputs), 2)
    }
    data.concrete_values[output.debugName()] = new_dict
    return None


@register_handler("prim::DictConstruct", num_outputs=1)
def handle_dict_construct(data: HandlerData) -> Iterator[PostprocessNode] | None:
    node = data.default_node
    node.data.delete = True
    yield node
