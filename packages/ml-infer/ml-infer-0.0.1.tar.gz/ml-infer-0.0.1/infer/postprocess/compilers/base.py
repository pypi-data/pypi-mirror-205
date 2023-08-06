from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict

from torch import Tensor
from torch.nn.utils.fusion import fuse_conv_bn_weights

from infer.postprocess.graph import PostprocessGraph


class Compiler(ABC):
    """Defines the base compiler class.

    The compiler takes in a graph and saves it to a target location. Additional
    arguments can control how the graph is compiled.
    """

    def __init__(self, graph: PostprocessGraph) -> None:
        self.graph = graph

    def preprocess(self) -> None:
        """Applies common preprocessing passes to the graph.

        The preprocessing steps that are performed are as follows:

        - Fuse batch norm parameters into the weights of preceeding
          convolutions or transposed convolutions
        - Removes nodes which should be deleted
        """

        for node_name, node in list(self.graph.gen_nodes()):
            if node.op == "aten::batch_norm":
                ((in_value, _),) = self.graph.in_edges(node_name)
                conv_node = self.graph.get_node_data(in_value)
                assert conv_node.op == "aten::conv2d", f"Expected batch norm after conv, not {conv_node.op=}"
                assert (conv_data := conv_node.data.conv2d) is not None
                assert (bn_data := node.data.batch_norm) is not None

                # Fuses the batch norm params into the convolution params.
                conv_w, conv_b = conv_data.weight, conv_data.bias
                bn_rm, bn_rv, bn_eps = bn_data.running_mean, bn_data.running_var, bn_data.eps
                bn_w, bn_b = bn_data.weight, bn_data.bias
                conv_w, conv_b = fuse_conv_bn_weights(conv_w, conv_b, bn_rm, bn_rv, bn_eps, bn_w, bn_b)
                conv_data.weight, conv_data.bias = conv_w, conv_b

                # Removes the node once it is fused.
                self.graph.remove_node_and_reconnect(node.name)

        self.graph.finalize()

    @abstractmethod
    def compile(self, save_dir: Path) -> None:
        """The main translation entry point.

        Args:
            save_dir: The path to save the compiled graph
        """

        raise NotImplementedError


class Engine(ABC):
    """Defines the base engine class.

    The engine takes in a compiled model and prepares it for doing inference.
    Inference is done on a list of Torch tensors.
    """

    def __init__(self, save_dir: Path) -> None:
        self.save_dir = save_dir

    @abstractmethod
    def infer(self, sample: Dict[str, Tensor]) -> Dict[str, Tensor]:
        """Runs inference for a single sample.

        Args:
            sample: The sample to run inference on

        Returns:
            The outputs of running inference on the sample
        """

    def __call__(self, sample: Dict[str, Tensor]) -> Dict[str, Tensor]:
        return self.infer(sample)
