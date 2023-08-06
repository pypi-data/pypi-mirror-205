import torch
from torch import Tensor, nn

from infer.cpp.inference.inference import observer_name
from infer.preprocess.init import preprocess_, run_preprocess_checks


class SimpleConvModule(nn.Module):
    def __init__(self, dims: int):
        super().__init__()

        self.conv = nn.Sequential(
            nn.Conv2d(dims, dims, 1),
            nn.BatchNorm2d(dims),
            nn.ReLU(),
        )

    def forward(self, x: Tensor) -> Tensor:
        return self.conv(x)


def test_conv_module() -> None:
    module = SimpleConvModule(16)
    input_tensor = torch.randn(1, 16, 8, 8)
    script_module = preprocess_(module, example_inputs=[(input_tensor,)])
    run_preprocess_checks(script_module)

    # Enables fake quantization.
    observer = getattr(script_module, observer_name())
    observer.set_fake_quantize_enabled(True)
    observer.set_observer_enabled(False)

    # Checks that the output tensor is reasonably quantized.
    output_tensor = script_module(input_tensor)
    num_unique_quants = output_tensor.unique().numel()
    assert 32 < num_unique_quants < 256
