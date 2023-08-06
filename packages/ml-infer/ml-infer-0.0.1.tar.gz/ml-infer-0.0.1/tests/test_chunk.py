from typing import Tuple

import torch
from torch import Tensor, nn

from infer.cpp.inference.inference import observer_name
from infer.preprocess.init import preprocess_, run_preprocess_checks


class ChunkModule(nn.Module):
    def __init__(self, dims: int) -> None:
        super().__init__()

        self.conv_a = nn.Sequential(nn.Conv2d(dims, dims, 1), nn.BatchNorm2d(dims), nn.ReLU6())
        self.conv_b = nn.Sequential(nn.Conv2d(dims, dims, 1), nn.BatchNorm2d(dims), nn.ReLU6())

    def forward(self, x: Tensor) -> Tuple[Tensor, Tensor]:
        a, b = torch.chunk(x, 2, dim=1)
        a, b = self.conv_a(a), self.conv_b(b)
        return a, b


def test_concat() -> None:
    module = ChunkModule(16)
    example_inputs = [(torch.randn(1, 32, 3, 4).clamp_min_(0.0),), (torch.randn(1, 32, 4, 4).clamp_min_(0.0),)]

    script_module = preprocess_(module, example_inputs=example_inputs)

    # Populates the observers.
    for (example_input,) in example_inputs:
        script_module(example_input)

    # Gets the observer object from the module.
    observer = getattr(script_module, observer_name())

    # Checks valid range observers.
    for range_id in range(observer.num_ranges()):
        range_val = observer.get_range(range_id)
        assert range_val is not None
        range_min, range_max = range_val
        assert range_min == 0
        assert range_max > 0

    # Checks valid shape observers.
    for shape_id in range(observer.num_shapes()):
        obs_shape = observer.get_shape(shape_id)
        assert obs_shape is not None
        assert len(obs_shape) == 4
        assert obs_shape[2:] == [None, 4]

    # At this point, the model should be exportable.
    run_preprocess_checks(script_module)
