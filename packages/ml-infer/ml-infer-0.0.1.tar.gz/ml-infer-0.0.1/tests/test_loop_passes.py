import pytest
import torch
from torch import Tensor, nn

from infer.cpp.inference.inference import NodeException
from infer.preprocess.init import preprocess_, run_preprocess_checks


class LoopModule(nn.Module):
    __constants__ = ["with_insert"]

    def __init__(self, with_insert: bool) -> None:
        super().__init__()

        self.with_insert = with_insert

    def forward(self, x: Tensor) -> Tensor:
        y1, y2 = [(x,), (x + 1,)], [(x,), (x - 1,)]
        y1[0] = (x,)
        for _ in range(31):
            for _ in range(32):
                if self.with_insert:
                    y1.insert(0, (x,))
                y1a, y1b = y1[:2]
                y1, y2 = [y2[1], y2[0]], [(y1b[0] + 1,), y1a]
        return y1[0][0]


def test_handle_loops() -> None:
    module = LoopModule(False)

    script_module = preprocess_(module, example_inputs=[(torch.randn(1, 2, 3, 4),)])

    # At this point, the model should be exportable.
    run_preprocess_checks(script_module)


def test_non_removable_loop() -> None:
    module = LoopModule(True)

    # Since there's an insertion here, the model should not be exported,
    # because the insertion makes it impossible to unpack the containers inside
    # the loop.
    with pytest.raises(NodeException):
        preprocess_(module, example_inputs=[(torch.randn(1, 2, 3, 4),)])
