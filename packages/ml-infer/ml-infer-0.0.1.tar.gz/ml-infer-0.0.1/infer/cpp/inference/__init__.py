"""Defines the C++ backend for the inference library."""

from pathlib import Path

import torch

from .inference import *  # noqa: F401,F403

# Registers the shared library with Torch.
torch.ops.load_library(Path(__file__).parent.resolve() / "inference.so")

# Access modules registered with `TORCH_LIBRARY` instead of `PYBIND11_MODULE`
TORCH = torch.ops.inference

# Cleans up variables which shouldn't be exported.
del torch, Path
