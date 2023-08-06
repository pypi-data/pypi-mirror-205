from __future__ import annotations

from typing import Iterator

from infer.postprocess.graph import EltwiseData, PostprocessNode
from infer.postprocess.handler import HandlerData, register_handler


@register_handler("aten::lt", num_inputs=2, num_outputs=1, implicit_inds=(0,))
@register_handler("aten::lt", num_inputs=2, num_outputs=1, implicit_inds=(1,))
@register_handler("aten::lt", num_inputs=2, num_outputs=1, implicit_inds=(0, 1))
@register_handler("aten::gt", num_inputs=2, num_outputs=1, implicit_inds=(0,))
@register_handler("aten::gt", num_inputs=2, num_outputs=1, implicit_inds=(1,))
@register_handler("aten::gt", num_inputs=2, num_outputs=1, implicit_inds=(0, 1))
@register_handler("aten::lte", num_inputs=2, num_outputs=1, implicit_inds=(0,))
@register_handler("aten::lte", num_inputs=2, num_outputs=1, implicit_inds=(1,))
@register_handler("aten::lte", num_inputs=2, num_outputs=1, implicit_inds=(0, 1))
@register_handler("aten::gte", num_inputs=2, num_outputs=1, implicit_inds=(0,))
@register_handler("aten::gte", num_inputs=2, num_outputs=1, implicit_inds=(1,))
@register_handler("aten::gte", num_inputs=2, num_outputs=1, implicit_inds=(0, 1))
@register_handler("aten::__and__", num_inputs=2, num_outputs=1, implicit_inds=(0,))
@register_handler("aten::__and__", num_inputs=2, num_outputs=1, implicit_inds=(1,))
@register_handler("aten::__and__", num_inputs=2, num_outputs=1, implicit_inds=(0, 1))
def handle_lt(data: HandlerData) -> Iterator[PostprocessNode] | None:
    node = data.default_node
    lhs_name, rhs_name = data.input_names[:2]
    lhs = data.concrete_values.get(lhs_name)
    rhs = data.concrete_values.get(rhs_name)
    assert lhs is None or isinstance(lhs, (int, float))
    assert rhs is None or isinstance(rhs, (int, float))
    node.data.eltwise = EltwiseData(lhs=lhs, rhs=rhs)
    yield node


@register_handler("aten::__and__", num_inputs=2, num_outputs=1, implicit_inds=(0, 1))
def handle_and(data: HandlerData) -> Iterator[PostprocessNode] | None:
    node = data.default_node
    lhs_name, rhs_name = data.input_names[:2]
    lhs = data.concrete_values.get(lhs_name)
    rhs = data.concrete_values.get(rhs_name)
    assert lhs is None or isinstance(lhs, (int, float))
    assert rhs is None or isinstance(rhs, (int, float))
    node.data.eltwise = EltwiseData(lhs=lhs, rhs=rhs)
    return None
