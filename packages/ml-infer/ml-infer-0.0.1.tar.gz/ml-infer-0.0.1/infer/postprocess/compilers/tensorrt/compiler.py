from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import tensorrt as trt  # pylint: disable=import-error
import torch
from torch import Tensor

from infer.postprocess.compilers.base import Compiler
from infer.postprocess.compilers.tensorrt.utils import (
    eltwise,
    get_const,
    layer_norm,
    linear,
    reduce,
)
from infer.postprocess.compilers.utils import Sizes, get_arr
from infer.postprocess.graph import PostprocessGraph, PostprocessNode

TRT_LOGGER = trt.Logger(trt.Logger.WARNING)

EXPLICIT_BATCH = 1 << (int)(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH)
EXPLICIT_PRECISION = 1 << (int)(trt.NetworkDefinitionCreationFlag.EXPLICIT_PRECISION)
CREATION_FLAGS = EXPLICIT_BATCH | EXPLICIT_PRECISION

ELTWISE_OPS = {
    "aten::add": trt.ElementWiseOperation.SUM,
    "aten::sub": trt.ElementWiseOperation.SUB,
    "aten::mul": trt.ElementWiseOperation.PROD,
    "aten::div": trt.ElementWiseOperation.DIV,
}


@dataclass
class TensorRTConfig:
    max_workspace_size_kilobytes: float = field(default=1_000_000)


def assert_not_none(i: int | None) -> int:
    assert i is not None, "CoreML compiler doesn't support broadcasting shapes yet"
    return i


def ones(i: int) -> List[int]:
    return [1] * i


def get_static_shape(shape: Iterable[int | None] | torch.Size) -> Tuple[int, ...]:
    """Converts from PyTorch shape to TensorRT-compatible shape.

    Args:
        shape: The PyTorch tensor shape

    Returns:
        The TensorRT-compatible shape
    """

    shape_concrete = [assert_not_none(i) for i in shape]
    rank = len(shape_concrete)
    assert 1 <= rank, f"Invalid {rank=}"

    if rank == 1:
        (b,), (c, h, w) = shape_concrete, ones(3)
    elif rank == 2:
        (b, c), (h, w) = shape_concrete, ones(2)
    elif rank == 3:
        (b, c, h), (w,) = shape_concrete, ones(1)
    elif rank == 4:
        b, c, h, w = shape_concrete
    else:
        return tuple(shape_concrete)

    return b, c, h, w


def rectify_static_dim(dim: int, rank: int) -> int:
    if rank == 1:
        inds = [0]
    elif rank == 2:
        inds = [0, 1]
    elif rank == 3:
        inds = [0, 1, 2]
    elif rank == 4:
        inds = [0, 1, 2, 3]
    else:
        inds = list(range(rank))

    return inds[dim]


def convert_to_static_shape(t: Tensor) -> Tensor:
    static_shape = get_static_shape(t.shape)
    return t.view(static_shape)


class TensorRTCompiler(Compiler):
    """Defines a translator for generating a TensorRT package."""

    def __init__(self, graph: PostprocessGraph, config: TensorRTConfig | None = None) -> None:
        super().__init__(graph)

        self.config = TensorRTConfig() if config is None else config

    def add_node(
        self,
        node: PostprocessNode,
        network: trt.INetworkDefinition,
        value_map: Dict[str, trt.ITensor],
    ) -> None:
        if node.op == "prim::Param":
            for o in node.outputs:
                shape = get_static_shape(node.get_shape(o))
                value_map[o] = network.add_input(name=o, dtype=trt.float32, shape=shape)
        elif node.op == "aten::conv1d":
            in_name, out_name = node.inputs[0], node.outputs[0]
            assert (conv1d_data := node.data.conv1d) is not None
            kernel, bias = get_arr(conv1d_data.weight), get_arr(conv1d_data.bias)
            kernel_shape = trt.Dims([kernel.shape[-1], 1])
            layer = network.add_convolution_nd(
                input=value_map[in_name],
                num_output_maps=kernel.shape[0],
                kernel_shape=kernel_shape,
                kernel=trt.Weights(kernel),
                bias=trt.Weights() if bias is None else trt.Weights(bias),
            )
            value_map[out_name] = layer.get_output(0)
        elif node.op == "aten::conv2d":
            in_name, out_name = node.inputs[0], node.outputs[0]
            assert (conv2d_data := node.data.conv2d) is not None
            kernel, bias = get_arr(conv2d_data.weight), get_arr(conv2d_data.bias)
            kernel_shape = trt.Dims([kernel.shape[-2], kernel.shape[-1]])
            layer = network.add_convolution_nd(
                input=value_map[in_name],
                num_output_maps=kernel.shape[0],
                kernel_shape=kernel_shape,
                kernel=trt.Weights(kernel),
                bias=trt.Weights() if bias is None else trt.Weights(bias),
            )
            value_map[out_name] = layer.get_output(0)
        elif node.op == "aten::linear":
            in_name, out_name = node.inputs[0], node.outputs[0]
            assert (linear_data := node.data.linear) is not None
            value_map[out_name] = linear(
                network=network,
                input_tensor=value_map[in_name],
                weight=linear_data.weight,
                bias=linear_data.bias,
            )
        elif node.op == "aten::matmul":
            (lhs_name, rhs_name), out_name = node.inputs, node.outputs[0]
            layer = network.add_matrix_multiply(
                input0=value_map[lhs_name],
                op0=trt.MatrixOperation.NONE,
                input1=value_map[rhs_name],
                op1=trt.MatrixOperation.NONE,
            )
            value_map[out_name] = layer.get_output(0)
        elif node.op == "aten::clamp":
            in_name, out_name = node.inputs[0], node.outputs[0]
            assert (clamp_data := node.data.clamp) is not None
            min_val, max_val = clamp_data.min_val, clamp_data.max_val
            assert min_val is not None or max_val is not None
            x = value_map[in_name]
            rank = len(x.shape)
            if max_val is None:
                if min_val == 0.0:
                    x = network.add_activation(input=x, type=trt.ActivationType.RELU).get_output(0)
                else:
                    x = eltwise(network, x, min_val, trt.ElementWiseOperation.MAX, rank)
            elif min_val is None:
                x = eltwise(network, x, min_val, trt.ElementWiseOperation.MIN, rank)
            else:
                x = eltwise(network, x, min_val, trt.ElementWiseOperation.MAX, rank)
                x = eltwise(network, x, max_val, trt.ElementWiseOperation.MIN, rank)
            value_map[out_name] = x
        elif node.op == "inference::cat":
            in_names, out_name = node.inputs, node.outputs[0]
            assert (concat_data := node.data.concat) is not None
            concat_layer = network.add_concatenation([value_map[in_name] for in_name in in_names])
            concat_layer.axis = concat_data.dim
            value_map[out_name] = concat_layer.get_output(0)
        elif node.op == "prim::Return":
            for in_name in node.inputs:
                network.mark_output(value_map[in_name])
        elif node.op == "aten::layer_norm":
            in_name, out_name = node.inputs[0], node.outputs[0]
            assert (layer_norm_data := node.data.layer_norm) is not None
            value_map[out_name] = layer_norm(
                network=network,
                input_tensor=value_map[in_name],
                weight=layer_norm_data.weight,
                bias=layer_norm_data.bias,
                eps=layer_norm_data.eps,
            )
        elif node.op == "aten::reshape":
            in_name, out_name = node.inputs[0], node.outputs[0]
            assert (reshape_data := node.data.reshape) is not None
            shuffle_layer = network.add_shuffle(value_map[in_name])
            shuffle_layer.reshape_dims = trt.Dims(get_static_shape(reshape_data.shape))
            value_map[out_name] = shuffle_layer.get_output(0)
        elif node.op == "aten::transpose":
            in_name, out_name = node.inputs[0], node.outputs[0]
            assert (transpose_data := node.data.transpose) is not None
            shuffle_layer = network.add_shuffle(value_map[in_name])
            dims = list(range(len(node.shapes[in_name])))
            dim_a, dim_b = transpose_data.dim_a, transpose_data.dim_b
            dims[dim_a], dims[dim_b] = dims[dim_b], dims[dim_a]
            shuffle_layer.first_transpose = tuple(dims)
            value_map[out_name] = shuffle_layer.get_output(0)
        elif node.op == "aten::sum":
            in_name, out_name = node.inputs[0], node.outputs[0]
            assert (sum_data := node.data.reduce_sum) is not None
            value_map[out_name] = reduce(
                network=network,
                input_tensor=value_map[in_name],
                op=trt.ReduceOperation.SUM,
                dims=[rectify_static_dim(dim, len(node.get_shape(out_name))) for dim in sum_data.dims],
                keep_dims=sum_data.keep_dim,
            )
        elif node.op == "aten::mean":
            in_name, out_name = node.inputs[0], node.outputs[0]
            assert (mean_data := node.data.reduce_mean) is not None
            value_map[out_name] = reduce(
                network=network,
                input_tensor=value_map[in_name],
                op=trt.ReduceOperation.AVG,
                dims=[rectify_static_dim(dim, len(node.get_shape(out_name))) for dim in mean_data.dims],
                keep_dims=mean_data.keep_dim,
            )
        elif node.op == "inference::new_tensor":
            out_name = node.outputs[0]
            assert (new_tensor_data := node.data.new_tensor) is not None
            value_map[out_name] = get_const(network, convert_to_static_shape(new_tensor_data.value))
        elif node.op in ELTWISE_OPS:
            out_name = node.outputs[0]
            assert (eltwise_data := node.data.eltwise) is not None
            opt_lhs_name: str | None
            opt_rhs_name: str | None
            if eltwise_data.lhs is None and eltwise_data.rhs is None:
                opt_lhs_name, opt_rhs_name = node.inputs
            elif eltwise_data.lhs is None:
                (opt_lhs_name,), opt_rhs_name = node.inputs, None
            elif eltwise_data.rhs is None:
                opt_lhs_name, (opt_rhs_name,) = None, node.inputs
            else:
                opt_lhs_name, opt_rhs_name = None, None
            lhs = eltwise_data.lhs if opt_lhs_name is None else value_map[opt_lhs_name]
            rhs = eltwise_data.rhs if opt_rhs_name is None else value_map[opt_rhs_name]
            rank = len(get_static_shape(node.get_shape(out_name)))
            value_map[out_name] = eltwise(network, lhs, rhs, ELTWISE_OPS[node.op], rank)
        elif node.op == "aten::square":
            in_name, out_name = node.inputs[0], node.outputs[0]
            value_map[out_name] = network.add_elementwise(
                input1=value_map[in_name],
                input2=get_const(network, 2.0, len(value_map[in_name].shape)),
                op=trt.ElementWiseOperation.POW,
            ).get_output(0)
        elif node.op == "aten::sqrt":
            in_name, out_name = node.inputs[0], node.outputs[0]
            value_map[out_name] = network.add_unary(
                input=value_map[in_name],
                op=trt.UnaryOperation.SQRT,
            ).get_output(0)
        elif node.op == "aten::sigmoid":
            in_name, out_name = node.inputs[0], node.outputs[0]
            value_map[out_name] = network.add_activation(
                input=value_map[in_name],
                type=trt.ActivationType.SIGMOID,
            ).get_output(0)
        elif node.op == "inference::chunk":
            in_name, out_names = node.inputs[0], node.outputs
            assert (chunk_data := node.data.chunk) is not None
            in_shape = node.get_shape(in_name)
            chunk_dim = rectify_static_dim(chunk_data.dim, len(in_shape))
            assert (full_chunk_size := in_shape[chunk_data.dim]) is not None
            assert full_chunk_size % chunk_data.num_chunks == 0
            chunk_size = full_chunk_size // chunk_data.num_chunks
            rect_in_shape = get_static_shape(in_shape)
            for i, out_name in enumerate(out_names):
                layer = network.add_slice(
                    input=value_map[in_name],
                    start=[i * chunk_size if j == chunk_dim else 0 for j, _ in enumerate(rect_in_shape)],
                    shape=[chunk_size if j == chunk_dim else s for j, s in enumerate(rect_in_shape)],
                    stride=[1] * len(rect_in_shape),
                )
                value_map[out_name] = layer.get_output(0)
        elif node.op == "aten::softmax":
            in_name, out_name = node.inputs[0], node.outputs[0]
            assert (softmax_data := node.data.softmax) is not None
            softmax_dim = rectify_static_dim(softmax_data.dim, len(node.get_shape(in_name)))
            layer = network.add_softmax(value_map[in_name])
            layer.axes = 1 << softmax_dim
            value_map[out_name] = layer.get_output(0)
        else:
            raise NotImplementedError(f"{node.op=} not implemented")

        for out_name in node.outputs:
            if out_name in value_map:
                assert value_map[out_name].shape == get_static_shape(node.shapes[out_name])

    def translate(self) -> Tuple[trt.Builder, trt.INetworkDefinition]:
        self.preprocess()

        builder = trt.Builder(TRT_LOGGER)
        network = builder.create_network(CREATION_FLAGS)
        value_map: Dict[str, trt.ITensor] = {}

        for _, node in self.graph.gen_nodes():
            self.add_node(node, network, value_map)

        return builder, network

    def compile(self, save_dir: Path) -> None:
        # Saves the initial graph.
        self.graph.save(save_dir / "model.graph")

        # Converts the graph to a network.
        builder, network = self.translate()

        # Creates the plan from from the network
        config = builder.create_builder_config()
        memory_pool_limit = Sizes.kb_to_bytes(self.config.max_workspace_size_kilobytes)
        config.set_memory_pool_limit(trt.MemoryPoolType.WORKSPACE, memory_pool_limit)
        plan = builder.build_serialized_network(network, config)
        with open(save_dir / "model.plan", "wb") as f:
            f.write(plan)

        # Creates CUDA engine and writes to disk.
        runtime = trt.Runtime(TRT_LOGGER)
        engine = runtime.deserialize_cuda_engine(plan)
        with open(save_dir / "model.engine", "wb") as f:
            f.write(engine.serialize())

        # Saves the spec as well.
        spec = self.graph.get_spec()
        spec.save(save_dir / "input_spec.json")


def compile_graph(graph: PostprocessGraph, save_dir: Path | str) -> None:
    """Short-hand function for calling the compiler.

    Args:
        graph: The graph to compile
        save_dir: Where to save the compiled package
    """

    TensorRTCompiler(graph).compile(Path(save_dir))
