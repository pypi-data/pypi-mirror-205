from __future__ import annotations

from typing import Iterator

from infer.postprocess.graph import (
    BatchNormData,
    Conv1dData,
    Conv2dData,
    PostprocessNode,
)
from infer.postprocess.handler import HandlerData, register_handler


@register_handler("aten::conv1d", num_inputs=7, num_outputs=1, implicit_inds=(0,))
def handle_conv1d(data: HandlerData) -> Iterator[PostprocessNode] | None:
    weight, bias, stride, padding, dilation, groups = (data.concrete_values[name] for name in data.input_names[1:])

    node = data.default_node
    node.data.conv1d = Conv1dData(
        weight=weight,
        bias=bias,
        stride=(stride[0],),
        padding=(padding[0],),
        dilation=(dilation[0],),
        groups=groups,
    )
    yield node


@register_handler("aten::conv2d", num_inputs=7, num_outputs=1, implicit_inds=(0,))
def handle_conv2d(data: HandlerData) -> Iterator[PostprocessNode] | None:
    weight, bias, stride, padding, dilation, groups = (data.concrete_values[name] for name in data.input_names[1:])

    node = data.default_node
    node.data.conv2d = Conv2dData(
        weight=weight,
        bias=bias,
        stride=(stride[0], stride[1]),
        padding=(padding[0], padding[1]),
        dilation=(dilation[0], dilation[1]),
        groups=groups,
    )
    yield node


@register_handler("aten::batch_norm", num_inputs=8, num_outputs=1, implicit_inds=(0,))
@register_handler("aten::batch_norm", num_inputs=9, num_outputs=1, implicit_inds=(0,))
def handle_batchnorm_concrete(data: HandlerData) -> Iterator[PostprocessNode] | None:
    concrete_values = (data.concrete_values[name] for name in data.input_names[1:8])
    weight, bias, running_mean, running_var, _, momentum, eps = concrete_values

    node = data.default_node
    node.data.batch_norm = BatchNormData(
        weight=weight,
        bias=bias,
        running_mean=running_mean,
        running_var=running_var,
        momentum=momentum,
        eps=eps,
    )
    yield node
