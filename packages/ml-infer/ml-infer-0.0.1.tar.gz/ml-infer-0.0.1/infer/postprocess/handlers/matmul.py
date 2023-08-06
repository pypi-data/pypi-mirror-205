from __future__ import annotations

from typing import Iterator

from infer.postprocess.graph import PostprocessNode
from infer.postprocess.handler import HandlerData, register_handler


@register_handler("aten::matmul", num_inputs=2, num_outputs=1, concrete=False)
def handle_matmul_implicit(data: HandlerData) -> Iterator[PostprocessNode] | None:
    node = data.default_node
    yield node
