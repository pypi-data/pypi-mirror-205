from __future__ import annotations

from typing import Iterator

from infer.postprocess.graph import LinearData, PostprocessNode
from infer.postprocess.handler import HandlerData, register_handler


@register_handler("aten::linear", num_inputs=3, num_outputs=1, implicit_inds=(0,))
def handle_linear_concrete(data: HandlerData) -> Iterator[PostprocessNode] | None:
    weight, bias = (data.concrete_values[name] for name in data.input_names[1:])

    node = data.default_node
    node.data.linear = LinearData(weight=weight, bias=bias)
    yield node
