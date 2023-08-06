# pylint: disable=stop-iteration-return

import os
from typing import Dict, Iterator, Tuple

import pytest
import torch
from torch import Tensor, nn

from infer.postprocess.compilers.auto import compile_graph, get_engine
from infer.postprocess.generate import generate
from infer.preprocess.init import preprocess_, run_preprocess_checks
from infer.utils.tests import assert_dicts_equal


class SimpleConvModule(nn.Module):
    def __init__(self, dim: int) -> None:
        super().__init__()

        self.conv_a = nn.Sequential(nn.Conv2d(dim, dim, 1), nn.BatchNorm2d(dim), nn.ReLU6())
        self.conv_b = nn.Sequential(nn.Conv2d(dim, dim, 1), nn.BatchNorm2d(dim), nn.ReLU6())
        self.conv_c = nn.Sequential(nn.Conv2d(dim, dim, 1), nn.BatchNorm2d(dim), nn.ReLU6())
        self.conv_d = nn.Sequential(nn.Conv2d(dim * 2, dim, 1, bias=False), nn.BatchNorm2d(dim), nn.ReLU6())
        self.conv_e = nn.Sequential(nn.Conv2d(dim * 2, dim, 1), nn.BatchNorm2d(dim), nn.ReLU6())

    def forward(self, x: Tensor) -> Tensor:
        a = self.conv_a(x)
        b = self.conv_b(x)
        c = self.conv_c(b)
        d = self.conv_d(torch.cat([a, c], dim=1))
        e = self.conv_e(torch.cat([b, d], dim=1))
        return e


class SimpleLinearModule(nn.Module):
    def __init__(self, dim: int) -> None:
        super().__init__()

        self.linear_a = nn.Linear(dim, dim)
        self.linear_b = nn.Linear(dim, dim)
        self.linear_c = nn.Linear(dim * 2, dim)

    def forward(self, x: Tensor) -> Tensor:
        a = self.linear_a(x)
        b = self.linear_b(x)
        c = self.linear_c(torch.cat((a, b), dim=-1))
        return c


def gen_modules() -> Iterator[Tuple[nn.Module, Tensor]]:
    yield SimpleConvModule(16), torch.randn(1, 16, 3, 4)
    yield SimpleLinearModule(16), torch.randn(1, 16)


def gen_modules_with_targets() -> Iterator[Tuple[nn.Module, Tensor, int, int, int]]:
    itr = gen_modules()
    yield *next(itr), 19, 18, 3
    yield *next(itr), 6, 5, 2


@pytest.mark.parametrize("module,input_tensor,num_nodes,num_values,graph_width", gen_modules_with_targets())
def test_postprocess_simple_conv_module(
    module: nn.Module,
    input_tensor: Tensor,
    num_nodes: int,
    num_values: int,
    graph_width: int,
    tmpdir: str,
) -> None:
    module.eval()
    script_module = preprocess_(module, example_inputs=[(input_tensor,)])
    run_preprocess_checks(script_module)
    postprocess_graph = generate(script_module)
    assert postprocess_graph.num_nodes == num_nodes
    assert postprocess_graph.num_values == num_values

    img_path = os.path.join(tmpdir, "graph.svg")
    spec = postprocess_graph.visualize(img_path)
    assert spec.width == graph_width


@pytest.mark.tensorrt
@pytest.mark.parametrize("module,input_tensor", gen_modules())
def test_tensorrt_simple_conv_module(module: nn.Module, input_tensor: Tensor, tmpdir: str) -> None:
    module.eval()
    script_module = preprocess_(module, example_inputs=[(input_tensor,)])
    postprocess_graph = generate(script_module)
    spec = postprocess_graph.get_spec()
    input_name, output_name = spec.inputs[0].name, spec.outputs[0].name
    torch_output: Dict[str, Tensor] = {output_name: script_module(input_tensor)}

    # Compiles the graph to the temporary directory.
    compile_graph("tensorrt", postprocess_graph, tmpdir)

    # Loads the compiled graph and runs inference on a single sample.
    engine = get_engine("tensorrt", tmpdir)
    engine_output: Dict[str, Tensor] = engine({input_name: input_tensor})

    # Checks that the engine output matches the Torch output.
    assert_dicts_equal(torch_output, engine_output)


@pytest.mark.coreml
@pytest.mark.parametrize("module,input_tensor", gen_modules())
def test_coreml_simple_conv_module(module: nn.Module, input_tensor: Tensor, tmpdir: str) -> None:
    module.eval()
    script_module = preprocess_(module, example_inputs=[(input_tensor,)])
    postprocess_graph = generate(script_module)
    spec = postprocess_graph.get_spec()
    input_name, output_name = spec.inputs[0].name, spec.outputs[0].name
    torch_output: Dict[str, Tensor] = {output_name: script_module(input_tensor)}

    # Compiltes the graph to the temporary directory.
    compile_graph("coreml", postprocess_graph, tmpdir)

    # Loads the compiled graph and runs inference on a single sample
    engine = get_engine("coreml", tmpdir)
    engine_output: Dict[str, Tensor] = engine({input_name: input_tensor})

    # Checks that the engine output matches the Torch output.
    assert_dicts_equal(torch_output, engine_output)
