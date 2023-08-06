"""Provides wrapper functions for abstracting backend from graph compilation."""

# pylint: disable=import-outside-toplevel

from __future__ import annotations

from pathlib import Path
from typing import Literal

from infer.postprocess.compilers.base import Engine
from infer.postprocess.graph import PostprocessGraph

Target = Literal["tensorrt", "coreml"]


def compile_graph(target: Target, graph: PostprocessGraph, save_dir: str | Path) -> None:
    if target == "tensorrt":
        try:
            from .tensorrt.compiler import compile_graph as compile_tensorrt_graph
        except Exception as e:
            raise RuntimeError("TensorRT compiler is not supported on this platform") from e
        return compile_tensorrt_graph(graph, save_dir)
    if target == "coreml":
        try:
            from .coreml.compiler import compile_graph as compile_coreml_graph
        except Exception as e:
            raise RuntimeError("CoreML compiler is not supported on this platform") from e
        return compile_coreml_graph(graph, save_dir)
    raise NotImplementedError(f"Unsupported target: {target}")


def get_engine(target: Target, save_dir: str | Path) -> Engine:
    if target == "tensorrt":
        try:
            from .tensorrt.engine import get_engine as get_tensorrt_engine
        except Exception as e:
            raise RuntimeError("TensorRT engine is not supported on this platform") from e
        return get_tensorrt_engine(save_dir)
    if target == "coreml":
        try:
            from .coreml.engine import get_engine as get_coreml_engine
        except Exception as e:
            raise RuntimeError("CoreML compiler is not supported on this platform") from e
        return get_coreml_engine(save_dir)
    raise NotImplementedError(f"Unsupported target: {target}")
