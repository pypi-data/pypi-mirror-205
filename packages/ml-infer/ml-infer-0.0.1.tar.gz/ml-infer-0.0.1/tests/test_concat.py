import torch
from torch import Tensor, nn

from infer.preprocess.init import preprocess_, run_preprocess_checks


class ConcatModule(nn.Module):
    def __init__(self, dims: int) -> None:
        super().__init__()

        self.conv_a = nn.Sequential(nn.Conv2d(dims, dims, 1), nn.BatchNorm2d(dims), nn.ReLU6())
        self.conv_b = nn.Sequential(nn.Conv2d(dims, dims, 1), nn.BatchNorm2d(dims), nn.ReLU6())

    def forward(self, x: Tensor) -> Tensor:
        a, b = self.conv_a(x), self.conv_b(x)
        return torch.cat([a, b], dim=1)


def test_concat() -> None:
    module = ConcatModule(16)

    script_module = preprocess_(module, example_inputs=[(torch.randn(1, 16, 3, 4),)])

    # At this point, the model should be exportable.
    run_preprocess_checks(script_module)
