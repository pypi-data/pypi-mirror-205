from __future__ import annotations

from pathlib import Path
from typing import Dict, Tuple

import coremltools as cm  # pylint: disable=import-error
import torch
from torch import Tensor

from infer.postprocess.compilers.base import Engine
from infer.postprocess.compilers.coreml.compiler import (
    MODEL_SPEC_NAME,
    convert_to_static_shape,
)
from infer.postprocess.compilers.utils import Spec


def fixup_shape(arr: Tensor, shape: Tuple[int | None, ...]) -> Tensor:
    shape_concrete = tuple(-1 if s is None else s for s in shape)
    return arr.view(shape_concrete)


class CoreMLEngine(Engine):
    """Defines engine for running Python-side inference of CoreML graphs."""

    def __init__(self, save_dir: Path) -> None:
        super().__init__(save_dir)

        # Loads the serialized spec to a model.
        spec_path = save_dir / MODEL_SPEC_NAME
        spec = cm.models.utils.load_spec(str(spec_path))
        self.model = cm.models.MLModel(spec)
        self.input_spec = Spec.load(save_dir / "input_spec.json")

    def infer(self, sample: Dict[str, Tensor]) -> Dict[str, Tensor]:
        inputs = {k: convert_to_static_shape(v).numpy() for k, v in sample.items()}
        preds = self.model.predict(inputs)
        true_shapes = {o.name: o.shape for o in self.input_spec.outputs}
        return {k: fixup_shape(torch.from_numpy(v), true_shapes[k]) for k, v in preds.items()}


def get_engine(save_dir: str | Path) -> CoreMLEngine:
    return CoreMLEngine(Path(save_dir))
