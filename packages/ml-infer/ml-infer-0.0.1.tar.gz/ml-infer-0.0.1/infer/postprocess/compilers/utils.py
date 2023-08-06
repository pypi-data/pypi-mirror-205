"""Defines some common helper functions for various compilers."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterator, List, Optional, Tuple, TypeVar, Union

import numpy as np
import torch
from torch import Tensor
from torch._C import Value

Array = Union[Tensor, np.ndarray]
OptArray = TypeVar("OptArray", Array, Optional[Array])


class Sizes:
    """Converts from bytes to larger values."""

    @staticmethod
    def kb_to_bytes(b: float) -> float:
        return b * (1 << 10)

    @staticmethod
    def mb_to_bytes(b: float) -> float:
        return b * (1 << 20)

    @staticmethod
    def gb_to_bytes(b: float) -> float:
        return b * (1 << 30)


def get_tensor_name(value: Value, skip_observer: bool = True) -> str:
    if skip_observer and value.node().kind() == "inference::observe":
        return value.node().inputsAt(1).debugName()
    else:
        return value.debugName()


def get_arr(data: OptArray) -> OptArray:
    if data is None:
        return None
    if isinstance(data, Tensor):
        return data.detach().to(torch.float32).cpu().numpy()
    return data


def get_input_obs_value(v: Value) -> Iterator[Value]:
    if v.node().kind() == "inference::observe":
        yield v
        return
    if len(v.uses()) != 1:
        return
    user = v.uses()[0].user
    if user.kind() != "inference::observe":
        return
    yield user.outputsAt(0)


def get_output_obs_value(v: Value) -> Iterator[Value]:
    kind = v.node().kind()
    if kind == "inference::observe":
        yield v
    elif kind == "prim::DictConstruct":
        inputs = list(v.node().inputs())
        for i in range(1, len(inputs), 2):
            yield from get_output_obs_value(inputs[i])  # pylint: disable=not-an-iterable
    elif kind == "prim::ListConstruct":
        for value in v.node().inputs():
            yield from get_output_obs_value(value)  # pylint: disable=not-an-iterable
    else:
        raise NotImplementedError(v.node().kind())


@dataclass
class SpecTensor:
    name: str
    shape: Tuple[int | None, ...]


@dataclass
class Spec:
    inputs: List[SpecTensor]
    outputs: List[SpecTensor]

    @classmethod
    def load(cls, save_path: str | Path) -> "Spec":
        with open(save_path, "r", encoding="utf-8") as f:
            s = json.load(f)
            return cls(
                inputs=[SpecTensor(**i) for i in s["inputs"]],
                outputs=[SpecTensor(**o) for o in s["outputs"]],
            )

    def save(self, save_path: str | Path) -> None:
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(asdict(self), f, indent=2)
