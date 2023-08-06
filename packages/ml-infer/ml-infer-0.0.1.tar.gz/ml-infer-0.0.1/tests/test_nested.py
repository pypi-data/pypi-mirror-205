import torch
from torch import Tensor, nn

from infer.cpp.inference.inference import observer_name
from infer.postprocess.generate import generate
from infer.preprocess.init import preprocess_, run_preprocess_checks


class InnerConv(nn.Module):
    __export_once__ = True

    def __init__(self) -> None:
        super().__init__()
        self.conv = nn.Conv2d(16, 16, 1)

    def forward(self, x: Tensor) -> Tensor:
        return self.conv(x)


class OuterConv(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.inner = InnerConv()
        self.conv = nn.Conv2d(16, 16, 1)

    def forward(self, x: Tensor) -> Tensor:
        return self.inner(self.conv(self.inner(x)))


def test_nested_modules() -> None:
    example_input = torch.randn(1, 16, 3, 4)
    module = OuterConv()
    module.to(torch.float32)

    script_module = preprocess_(module, [(example_input,)])

    # Gets the observer object from the module.
    observer = getattr(script_module, observer_name())

    # Checks valid range observers.
    for range_id in range(observer.num_ranges()):
        is_fp = observer.is_floating_point(range_id)
        assert is_fp is not None
        if is_fp:
            range_val = observer.get_range(range_id)
            assert range_val is not None

    # Checks valid shape observers.q
    for shape_id in range(observer.num_shapes()):
        obs_shape = observer.get_shape(shape_id)
        assert obs_shape is not None

    run_preprocess_checks(script_module)
    postprocess_graph = generate(script_module)
    assert postprocess_graph.num_nodes == 5
    assert postprocess_graph.num_values == 4
