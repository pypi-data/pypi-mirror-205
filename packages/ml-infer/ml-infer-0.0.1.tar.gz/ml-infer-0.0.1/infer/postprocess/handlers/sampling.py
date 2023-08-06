from __future__ import annotations

from typing import Iterator

from infer.postprocess.graph import MultinomialData, PostprocessNode
from infer.postprocess.handler import HandlerData, register_handler


@register_handler("aten::multinomial", num_inputs=4, num_outputs=1, implicit_inds=(0,))
def handle_multinomial(data: HandlerData) -> Iterator[PostprocessNode] | None:
    num_samples, replacement, generator = (data.concrete_values[name] for name in data.input_names[1:])
    assert generator is None
    node = data.default_node
    node.data.multinomial = MultinomialData(num_samples=num_samples, replacement=replacement)
    yield node
