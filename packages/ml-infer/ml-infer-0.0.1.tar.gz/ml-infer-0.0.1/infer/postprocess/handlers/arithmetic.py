from __future__ import annotations

from typing import Any, Callable, Iterator, Union, cast

import torch
from torch import Tensor
from torch._C import Value

from infer.postprocess.graph import EltwiseData, MaskedFillData, PostprocessNode
from infer.postprocess.handler import HandlerData, register_handler

Number = Union[int, float]


def handle_concrete_arithmetic(data: HandlerData, func: Callable[[Number, Number], Number]) -> None:
    assert data.num_inputs in (2, 3)
    if data.num_inputs == 3:
        assert data.concrete_values[data.input_names[2]] == 1
    lhs, rhs = (data.concrete_values[i] for i in data.input_names[:2])
    data.concrete_values[data.output_name] = func(lhs, rhs)


def handle_implicit_arithmetic(data: HandlerData) -> Iterator[PostprocessNode]:
    assert data.num_inputs in (2, 3)
    if data.num_inputs == 3:
        assert data.concrete_values[data.input_names[2]] == 1
    node = data.default_node
    lhs_name, rhs_name = data.input_names[:2]
    lhs = data.concrete_values.get(lhs_name)
    rhs = data.concrete_values.get(rhs_name)

    if isinstance(lhs, Tensor):
        lhs_node = data.new_tensor_node(lhs_name, lhs)
        yield lhs_node
        lhs = None

    if isinstance(rhs, Tensor):
        rhs_node = data.new_tensor_node(rhs_name, rhs)
        yield rhs_node
        rhs = None

    assert lhs is None or isinstance(lhs, (int, float))
    assert rhs is None or isinstance(rhs, (int, float))

    node.data.eltwise = EltwiseData(lhs, rhs)
    node.inputs = [i for i, j in ((lhs_name, lhs), (rhs_name, rhs)) if j is None]

    yield node


@register_handler("aten::add", num_inputs=2, num_outputs=1, concrete=True)
@register_handler("aten::add", num_inputs=3, num_outputs=1, concrete=True)
def handle_add_concrete(data: HandlerData) -> Iterator[PostprocessNode] | None:
    handle_concrete_arithmetic(data, lambda a, b: a + b)
    return None


@register_handler("aten::add", num_inputs=2, num_outputs=1, implicit_inds=(0,))
@register_handler("aten::add", num_inputs=3, num_outputs=1, implicit_inds=(0,))
@register_handler("aten::add", num_inputs=2, num_outputs=1, implicit_inds=(1,))
@register_handler("aten::add", num_inputs=3, num_outputs=1, implicit_inds=(1,))
@register_handler("aten::add", num_inputs=3, num_outputs=1, implicit_inds=(0, 1))
@register_handler("aten::add", num_inputs=2, num_outputs=1, concrete=False)
def handle_add_implicit(data: HandlerData) -> Iterator[PostprocessNode] | None:
    yield from handle_implicit_arithmetic(data)


@register_handler("aten::sub", num_inputs=2, num_outputs=1, concrete=True)
@register_handler("aten::sub", num_inputs=3, num_outputs=1, concrete=True)
def handle_sub_concrete(data: HandlerData) -> Iterator[PostprocessNode] | None:
    handle_concrete_arithmetic(data, lambda a, b: a - b)
    return None


@register_handler("aten::sub", num_inputs=2, num_outputs=1, implicit_inds=(0,))
@register_handler("aten::sub", num_inputs=3, num_outputs=1, implicit_inds=(0,))
@register_handler("aten::sub", num_inputs=2, num_outputs=1, implicit_inds=(1,))
@register_handler("aten::sub", num_inputs=3, num_outputs=1, implicit_inds=(1,))
@register_handler("aten::sub", num_inputs=3, num_outputs=1, implicit_inds=(0, 1))
@register_handler("aten::sub", num_inputs=2, num_outputs=1, concrete=False)
def handle_sub_implicit(data: HandlerData) -> Iterator[PostprocessNode] | None:
    yield from handle_implicit_arithmetic(data)


@register_handler("aten::floordiv", num_inputs=2, num_outputs=1, concrete=True)
@register_handler("aten::floordiv", num_inputs=3, num_outputs=1, concrete=True)
def handle_floordiv_concrete(data: HandlerData) -> Iterator[PostprocessNode] | None:
    handle_concrete_arithmetic(data, lambda a, b: a // b)
    return None


@register_handler("aten::floordiv", num_inputs=2, num_outputs=1, implicit_inds=(0,))
@register_handler("aten::floordiv", num_inputs=3, num_outputs=1, implicit_inds=(0,))
@register_handler("aten::floordiv", num_inputs=2, num_outputs=1, implicit_inds=(1,))
@register_handler("aten::floordiv", num_inputs=3, num_outputs=1, implicit_inds=(1,))
@register_handler("aten::floordiv", num_inputs=3, num_outputs=1, implicit_inds=(0, 1))
@register_handler("aten::floordiv", num_inputs=2, num_outputs=1, concrete=False)
def handle_floordiv_implicit(data: HandlerData) -> Iterator[PostprocessNode] | None:
    yield from handle_implicit_arithmetic(data)


@register_handler("aten::div", num_inputs=2, num_outputs=1, concrete=True)
@register_handler("aten::div", num_inputs=3, num_outputs=1, concrete=True)
def handle_div_concrete(data: HandlerData) -> Iterator[PostprocessNode] | None:
    handle_concrete_arithmetic(data, lambda a, b: a / b)
    return None


@register_handler("aten::div", num_inputs=2, num_outputs=1, implicit_inds=(0,))
@register_handler("aten::div", num_inputs=3, num_outputs=1, implicit_inds=(0,))
@register_handler("aten::div", num_inputs=2, num_outputs=1, implicit_inds=(1,))
@register_handler("aten::div", num_inputs=3, num_outputs=1, implicit_inds=(1,))
@register_handler("aten::div", num_inputs=3, num_outputs=1, implicit_inds=(0, 1))
@register_handler("aten::div", num_inputs=2, num_outputs=1, concrete=False)
def handle_div_implicit(data: HandlerData) -> Iterator[PostprocessNode] | None:
    yield from handle_implicit_arithmetic(data)


@register_handler("aten::mul", num_inputs=2, num_outputs=1, concrete=True)
@register_handler("aten::mul", num_inputs=3, num_outputs=1, concrete=True)
def handle_mul_concrete(data: HandlerData) -> Iterator[PostprocessNode] | None:
    handle_concrete_arithmetic(data, lambda a, b: a * b)
    return None


@register_handler("aten::mul", num_inputs=2, num_outputs=1, implicit_inds=(0,))
@register_handler("aten::mul", num_inputs=3, num_outputs=1, implicit_inds=(0,))
@register_handler("aten::mul", num_inputs=2, num_outputs=1, implicit_inds=(1,))
@register_handler("aten::mul", num_inputs=3, num_outputs=1, implicit_inds=(1,))
@register_handler("aten::mul", num_inputs=3, num_outputs=1, implicit_inds=(0, 1))
@register_handler("aten::mul", num_inputs=2, num_outputs=1, concrete=False)
def handle_mul_implicit(data: HandlerData) -> Iterator[PostprocessNode] | None:
    yield from handle_implicit_arithmetic(data)


@register_handler("aten::neg", num_inputs=1, num_outputs=1, concrete=True)
def handle_neg_concrete(data: HandlerData) -> Iterator[PostprocessNode] | None:
    data.concrete_values[data.output_name] = -data.concrete_values[data.input_name]
    return None


@register_handler("aten::neg", num_inputs=1, num_outputs=1, concrete=False)
def handle_neg_implicit(data: HandlerData) -> Iterator[PostprocessNode] | None:
    yield data.default_node


@register_handler("aten::masked_fill", num_inputs=3, num_outputs=1, implicit_inds=(0,))
@register_handler("aten::masked_fill_", num_inputs=3, num_outputs=1, implicit_inds=(0,))
def handle_masked_fill(data: HandlerData) -> Iterator[PostprocessNode] | None:
    mask, value = (data.concrete_values[name] for name in data.input_names[1:])

    node = data.default_node
    node.data.masked_fill = MaskedFillData(mask=mask, value=value)
    yield node


@register_handler("aten::pow", num_inputs=2, num_outputs=1, implicit_inds=(0,))
def handle_pow_implicit(data: HandlerData) -> Iterator[PostprocessNode] | None:
    power = data.concrete_values[data.input_names[1]]

    # Special case for squaring a number, since it is just a multiplication.
    if power == 2:
        node = data.default_node
        node.op = "aten::square"
        yield node
    else:
        yield from handle_implicit_arithmetic(data)


@register_handler("aten::sqrt", num_inputs=1, num_outputs=1, concrete=False)
def handle_sqrt_implicit(data: HandlerData) -> Iterator[PostprocessNode] | None:
    yield data.default_node


@register_handler("aten::eq", num_inputs=2, num_outputs=1, concrete=False)
def handle_eq_concrete(data: HandlerData) -> Iterator[PostprocessNode] | None:
    handle_concrete_arithmetic(data, cast(Callable[[Number, Number], Number], torch.eq))
    return None


@register_handler("aten::eq", num_inputs=2, num_outputs=1, implicit_inds=(0,))
@register_handler("aten::eq", num_inputs=2, num_outputs=1, implicit_inds=(1,))
@register_handler("aten::eq", num_inputs=2, num_outputs=1, concrete=False)
def handle_eq_implicit(data: HandlerData) -> Iterator[PostprocessNode] | None:
    yield from handle_implicit_arithmetic(data)


def resolve_is(implicit_tensor: Value, concrete_val: Any) -> bool:
    if concrete_val is None:
        tensor_kind = implicit_tensor.type().kind()
        if tensor_kind == "OptionalType":
            raise NotImplementedError("Implicit t")
        raise NotImplementedError(f"Type resolution for {tensor_kind} not implemented")
    raise NotImplementedError(f"Type resolution for {type(concrete_val)} not implemented")


@register_handler("aten::__isnot__", num_inputs=2, num_outputs=1, implicit_inds=(0,))
def handle_is_not(data: HandlerData) -> Iterator[PostprocessNode] | None:
    implicit_tensor = data.node.inputsAt(0)
    concrete_val = data.concrete_values[data.input_names[1]]
    data.concrete_values[data.output_name] = not resolve_is(implicit_tensor, concrete_val)
    return None


@register_handler("aten::square", num_inputs=1, num_outputs=1, implicit_inds=(0,))
def handle_square(data: HandlerData) -> Iterator[PostprocessNode] | None:
    yield data.default_node
