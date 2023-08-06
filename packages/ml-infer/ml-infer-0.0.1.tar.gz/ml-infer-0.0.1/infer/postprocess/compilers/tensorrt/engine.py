from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pycuda.autoinit  # noqa, pylint: disable=unused-import,import-error
import pycuda.driver as cuda  # pylint: disable=import-error
import tensorrt as trt  # pylint: disable=import-error
import torch
from torch import Tensor

from infer.postprocess.compilers.base import Engine
from infer.postprocess.compilers.tensorrt.compiler import convert_to_static_shape
from infer.postprocess.compilers.utils import Spec

TRT_LOGGER = trt.Logger(trt.Logger.WARNING)


@dataclass
class HostDeviceMem:
    host_mem: np.ndarray
    device_mem: np.ndarray


def fixup_shape(arr: Tensor, shape: Tuple[int | None, ...]) -> Tensor:
    shape_concrete = tuple(-1 if s is None else s for s in shape)
    return arr.view(shape_concrete)


class TensorRTEngine(Engine):
    """Defines engine for running Python-side inference of TensorRT graphs."""

    def __init__(self, save_dir: Path) -> None:
        super().__init__(save_dir)

        self.runtime = trt.Runtime(TRT_LOGGER)
        with open(save_dir / "model.plan", "rb") as f:
            self.engine = self.runtime.deserialize_cuda_engine(f.read())
        self.input_spec = Spec.load(save_dir / "input_spec.json")

        self.input_bufs, self.output_bufs, self.bindings, self.stream = self.allocate_buffers()
        self.context = self.engine.create_execution_context()

    def allocate_buffers(self) -> Tuple[List[HostDeviceMem], List[HostDeviceMem], List[int], cuda.Stream]:
        inputs: List[HostDeviceMem] = []
        outputs: List[HostDeviceMem] = []
        bindings: List[int] = []
        stream = cuda.Stream()
        for binding in self.engine:
            size = tuple(self.engine.get_binding_shape(binding))
            dtype = trt.nptype(self.engine.get_binding_dtype(binding))
            host_mem = cuda.pagelocked_empty(size, dtype)
            device_mem = cuda.mem_alloc(host_mem.nbytes)
            bindings.append(int(device_mem))
            if self.engine.binding_is_input(binding):
                inputs.append(HostDeviceMem(host_mem, device_mem))
            else:
                outputs.append(HostDeviceMem(host_mem, device_mem))
        return inputs, outputs, bindings, stream

    def infer(self, sample: Dict[str, Tensor]) -> Dict[str, Tensor]:
        assert len(self.input_bufs) == len(sample), f"Unexpected {len(sample)=}; expected {len(self.input_bufs)}"

        # Converts the sample dictionary to a list, to match TensorRT format.
        sample_list = [convert_to_static_shape(sample[i.name]) for i in self.input_spec.inputs]

        # Copies inputs to buffers.
        for input_buf, input_samp in zip(self.input_bufs, sample_list):
            np.copyto(input_buf.host_mem, input_samp.numpy())

        # Moves sample inputs to device.
        for input_buf in self.input_bufs:
            cuda.memcpy_htod_async(input_buf.device_mem, input_buf.host_mem, self.stream)

        # Runs execution.
        self.context.execute_async_v2(self.bindings, stream_handle=self.stream.handle)

        # Moves outputs to host.
        for output_buf in self.output_bufs:
            cuda.memcpy_dtoh_async(output_buf.host_mem, output_buf.device_mem, self.stream)

        # Synchronizes the stream.
        self.stream.synchronize()

        # Returns the host outputs.
        return_values = [torch.from_numpy(output_buf.host_mem) for output_buf in self.output_bufs]

        return {
            o.name: fixup_shape(return_value, o.shape)
            for o, return_value in zip(self.input_spec.outputs, return_values)
        }


def get_engine(save_dir: str | Path) -> TensorRTEngine:
    return TensorRTEngine(Path(save_dir))
