from __future__ import annotations

from typing import Iterator

from infer.postprocess.graph import PostprocessNode
from infer.postprocess.handler import HandlerData, register_handler


@register_handler("inference::observe", num_inputs=2, num_outputs=1, implicit_inds=(1,))
def handle_observe(data: HandlerData) -> Iterator[PostprocessNode] | None:
    node = data.default_node
    node.data.delete = True
    yield node


@register_handler("inference::observe", num_inputs=2, num_outputs=1, concrete=True)
def handle_observe_concrete(data: HandlerData) -> Iterator[PostprocessNode] | None:
    observer, tensor = (data.concrete_values[i] for i in data.input_names)

    # Turns on quantization and calls the observer.
    observe_method = observer._get_method("observe")
    observer._get_method("set_fake_quantize_enabled")(True)
    observer._get_method("set_observer_enabled")(False)
    observer._get_method("set_track_quant_stats")(False)

    range_id, shape_id = data.node.i("range"), data.node.i("shape")
    tensor_id, is_output = data.node.i("tensor"), data.node.i("output")
    output_tensor = observe_method(tensor, (range_id, shape_id, tensor_id, is_output != 0))

    data.concrete_values[data.output_name] = output_tensor
    return None
