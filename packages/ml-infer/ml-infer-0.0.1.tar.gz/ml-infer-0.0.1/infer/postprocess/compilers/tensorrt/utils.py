from __future__ import annotations

from typing import Sequence

import numpy as np
import tensorrt as trt  # pylint: disable=import-error
from torch import Tensor

from infer.postprocess.compilers.utils import get_arr
from infer.postprocess.handlers.utils import rectify_dim


def get_const(network: trt.INetworkDefinition, value: Tensor | np.ndarray | int | float, dims: int = 1) -> trt.ITensor:
    if isinstance(value, Tensor):
        arr = value.detach().float().cpu().numpy()
        return network.add_constant(tuple(arr.shape), trt.Weights(arr)).get_output(0)
    arr = np.ascontiguousarray([value], dtype=np.float32)
    return network.add_constant((1,) * dims, trt.Weights(arr)).get_output(0)


def layer_norm(
    network: trt.INetworkDefinition,
    input_tensor: trt.ITensor,
    weight: Tensor | None,
    bias: Tensor | None,
    eps: float = 1e-6,
) -> trt.ITensor:
    """Converts layernorm node to TensorRT nodes.

    Args:
        network: The network definition
        input_tensor: The input tensor value
        weight: Layer norm weight
        bias: Layer norm bias
        eps: Epsilon value for layernorm

    Returns:
        The normalized inputs (output of the layernorm operation)
    """

    mean = network.add_reduce(input_tensor, trt.ReduceOperation.AVG, axes=4, keep_dims=True).get_output(0)
    diff = network.add_elementwise(input_tensor, mean, trt.ElementWiseOperation.SUB).get_output(0)
    x = network.add_elementwise(
        input1=diff,
        input2=get_const(network, 2.0, len(diff.shape)),
        op=trt.ElementWiseOperation.POW,
    ).get_output(0)
    x = network.add_reduce(x, trt.ReduceOperation.AVG, axes=4, keep_dims=True).get_output(0)
    x = network.add_elementwise(x, get_const(network, eps, len(x.shape)), trt.ElementWiseOperation.MAX).get_output(0)
    std = network.add_unary(x, trt.UnaryOperation.SQRT).get_output(0)
    normalized_inputs = network.add_elementwise(diff, std, trt.ElementWiseOperation.DIV).get_output(0)
    if weight is not None or bias is not None:
        assert weight is not None and bias is not None, "Both weight and bias should be non-null"
        normalized_inputs = network.add_scale_nd(
            normalized_inputs,
            mode=trt.ScaleMode.CHANNEL,
            scale=trt.Weights(get_arr(weight)),
            shift=trt.Weights(get_arr(bias)),
            channel_axis=len(input_tensor.shape) - 1,
        ).get_output(0)
    return normalized_inputs


def linear_with_matmul(
    network: trt.INetworkDefinition,
    input_tensor: trt.ITensor,
    weight: Tensor,
    bias: Tensor | None,
) -> trt.ITensor:
    """Converts fully connected layer to TensorRT nodes.

    NOTE: This is supposed to implement the fix for the warning in the
    `add_fully_connected` call, but it doesn't seem to work properly.

    Args:
        network: The network definition
        input_tensor: The input tensor value
        weight: The linear layer weight
        bias: The linear layer bias

    Returns:
        The newly-created TensorRT node
    """

    w = network.add_constant(weight.shape, trt.Weights(get_arr(weight))).get_output(0)
    x = network.add_matrix_multiply(
        input0=input_tensor,
        op0=trt.MatrixOperation.NONE,
        input1=w,
        op1=trt.MatrixOperation.TRANSPOSE,
    ).get_output(0)

    if bias is None:
        return x

    # For some reason scale layers don't work.
    # x = network.add_scale_nd(
    #     x,
    #     mode=trt.ScaleMode.CHANNEL,
    #     scale=trt.Weights(get_arr(torch.zeros_like(bias))),
    #     shift=trt.Weights(get_arr(bias)),
    #     channel_axis=len(input_tensor.shape) - 1,
    # ).get_output(0)

    bias_expanded = bias.view((1,) * (len(x.shape) - len(bias.shape)) + tuple(bias.shape))
    b = network.add_constant(bias_expanded.shape, trt.Weights(get_arr(bias_expanded))).get_output(0)
    x = network.add_elementwise(
        input1=x,
        input2=b,
        op=trt.ElementWiseOperation.SUM,
    ).get_output(0)

    return x


def linear(
    network: trt.INetworkDefinition,
    input_tensor: trt.ITensor,
    weight: Tensor,
    bias: Tensor | None,
) -> trt.ITensor:
    """Converts fully connected layer to TensorRT nodes.

    Args:
        network: The network definition
        input_tensor: The input tensor value
        weight: The linear layer weight
        bias: The linear layer bias

    Returns:
        The newly-created TensorRT node

    Raises:
        ValueError: If the shape is incorrect
    """

    shape = list(input_tensor.shape)
    if len(shape) != 4 or any(i != 1 for i in shape[2:]):
        raise ValueError(f"Use `conv` instead of `linear` for input shape {input_tensor.shape}")

    if bias is None:
        x = network.add_fully_connected(
            input_tensor,
            num_outputs=weight.shape[0],
            kernel=trt.Weights(get_arr(weight)),
        ).get_output(0)
    else:
        x = network.add_fully_connected(
            input_tensor,
            num_outputs=weight.shape[0],
            kernel=trt.Weights(get_arr(weight)),
            bias=trt.Weights(get_arr(bias)),
        ).get_output(0)

    return x


def reduce(
    network: trt.INetworkDefinition,
    input_tensor: trt.ITensor,
    op: trt.ReduceOperation,
    dims: Sequence[int],
    keep_dims: bool,
) -> trt.ITensor:
    """Produces a reduce operation for a given set of dimensions.

    Args:
        network: The network definition
        input_tensor: The input tensor value
        op: The reduction op to apply
        dims: The dimensions to reduce
        keep_dims: If the dimension should be kept or not

    Returns:
        The output of the reduce operation
    """

    rank = len(input_tensor.shape)
    dims = [rectify_dim(dim, rank) for dim in dims]

    axis_mask = 0
    for dim in dims:
        axis_mask |= 1 << dim

    return network.add_reduce(input=input_tensor, op=op, axes=axis_mask, keep_dims=keep_dims).get_output(0)


def eltwise(
    network: trt.INetworkDefinition,
    lhs: trt.ITensor | int | float,
    rhs: trt.ITensor | int | float,
    op: trt.ElementWiseOperation,
    rank: int,
) -> trt.ITensor:
    """Produces an elementwise operation.

    Args:
        network: The network definition
        lhs: The left-hand side tensor value
        rhs: The right-hand side tensor value
        op: The elementwise operation to apply
        rank: The output tensor rank

    Returns:
        The output of the elementwise operation
    """

    lhs_concrete = isinstance(lhs, (int, float, Tensor))
    rhs_concrete = isinstance(rhs, (int, float, Tensor))

    if lhs_concrete and rhs_concrete:
        lhs = get_const(network, lhs, rank)
        rhs = get_const(network, rhs, rank)
    elif lhs_concrete:
        lhs = get_const(network, lhs, rank)
    elif rhs_concrete:
        rhs = get_const(network, rhs, rank)

    x = network.add_elementwise(
        input1=lhs,
        input2=rhs,
        op=op,
    ).get_output(0)

    assert len(x.shape) == rank

    return x
