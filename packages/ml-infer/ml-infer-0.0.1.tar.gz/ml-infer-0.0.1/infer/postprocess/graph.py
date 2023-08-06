from __future__ import annotations

import functools
import pickle
import random
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import ClassVar, DefaultDict, Dict, Iterator, List, Set, Tuple

import matplotlib.pyplot as plt
import networkx as nx
from torch import Tensor
from torch._C import Value

from infer.postprocess.compilers.utils import Spec, SpecTensor
from infer.utils.data_structures import LinkedList

NODE = "node"
VALUE = "value"


@dataclass
class NewTensorData:
    value: Tensor


@dataclass
class Conv1dData:
    weight: Tensor
    bias: Tensor | None
    stride: Tuple[int]
    padding: Tuple[int]
    dilation: Tuple[int]
    groups: int


@dataclass
class Conv2dData:
    weight: Tensor
    bias: Tensor | None
    stride: Tuple[int, int]
    padding: Tuple[int, int]
    dilation: Tuple[int, int]
    groups: int


@dataclass
class LinearData:
    weight: Tensor
    bias: Tensor | None


@dataclass
class BatchNormData:
    weight: Tensor | None
    bias: Tensor | None
    running_mean: Tensor | None
    running_var: Tensor | None
    momentum: float
    eps: float


@dataclass
class ClampData:
    min_val: float | None
    max_val: float | None


@dataclass
class SoftmaxData:
    dim: int


@dataclass
class ArgmaxData:
    dim: int
    keep_dim: bool


@dataclass
class ConcatData:
    dim: int


@dataclass
class SliceData:
    dim: int
    start: int
    end: int
    step: int


@dataclass
class SelectData:
    dim: int
    index: int


@dataclass
class EltwiseData:
    lhs: int | float | None
    rhs: int | float | None


@dataclass
class MaskedFillData:
    mask: Tensor
    value: float


@dataclass
class ReshapeData:
    shape: Tuple[int | None, ...]


@dataclass
class TransposeData:
    dim_a: int
    dim_b: int


@dataclass
class ChunkData:
    dim: int
    num_chunks: int


@dataclass
class LayerNormData:
    shape: Tuple[int, ...]
    weight: Tensor | None
    bias: Tensor | None
    eps: float


@dataclass
class ReduceSumData:
    dims: Tuple[int, ...]
    keep_dim: bool


@dataclass
class ReduceMeanData:
    dims: Tuple[int, ...]
    keep_dim: bool


@dataclass
class MultinomialData:
    num_samples: int
    replacement: bool


@dataclass
class IfStatementData:
    condition: str
    if_true_inputs: List[str]
    if_true_outputs: List[str]
    if_false_inputs: List[str]
    if_false_outputs: List[str]


@dataclass
class LoopStatementData:
    condition: str
    trip_count: str
    counter_input: str
    counter_output: str
    inputs: List[str]
    outputs: List[str]


@dataclass
class PostprocessNodeData:
    new_tensor: NewTensorData | None = field(default=None)
    conv1d: Conv1dData | None = field(default=None)
    conv2d: Conv2dData | None = field(default=None)
    linear: LinearData | None = field(default=None)
    batch_norm: BatchNormData | None = field(default=None)
    clamp: ClampData | None = field(default=None)
    softmax: SoftmaxData | None = field(default=None)
    argmax: ArgmaxData | None = field(default=None)
    concat: ConcatData | None = field(default=None)
    slice: SliceData | None = field(default=None)
    select: SelectData | None = field(default=None)
    eltwise: EltwiseData | None = field(default=None)
    masked_fill: MaskedFillData | None = field(default=None)
    reshape: ReshapeData | None = field(default=None)
    transpose: TransposeData | None = field(default=None)
    chunk: ChunkData | None = field(default=None)
    layer_norm: LayerNormData | None = field(default=None)
    reduce_sum: ReduceSumData | None = field(default=None)
    reduce_mean: ReduceMeanData | None = field(default=None)
    multinomial: MultinomialData | None = field(default=None)
    if_statement: IfStatementData | None = field(default=None)
    loop_statement: LoopStatementData | None = field(default=None)
    delete: bool = field(default=False)


@dataclass
class PostprocessNode:
    op: str
    inputs: List[str] = field(default_factory=lambda: [])
    outputs: List[str] = field(default_factory=lambda: [])
    data: PostprocessNodeData = field(default_factory=PostprocessNodeData)
    shapes: Dict[str, Tuple[int | None, ...]] = field(default_factory=dict)
    ranges: Dict[str, Tuple[float, float]] = field(default_factory=dict)

    # Counter used for giving each node a unique name.
    global_counter: ClassVar[int] = 1

    @functools.cached_property
    def name(self) -> str:
        # if len(self.outputs) != 0:
        #     return f"node:{'.'.join(self.outputs)}"
        PostprocessNode.global_counter += 1
        return f"node:global_node_{self.global_counter}"

    def __str__(self) -> str:
        input_str = f"inputs: {', '.join(f'[{v.name}]' for v in self.inputs)}" if self.inputs else None
        output_str = f"outputs: {', '.join(f'[{v.name}]' for v in self.outputs)}" if self.outputs else None
        parts = [self.op] + [i for i in (input_str, output_str) if i is not None]
        return "\n  ".join(parts)

    @classmethod
    def get_bridge(cls, input_val: Value, output_val: Value) -> "PostprocessNode":
        node = cls(
            op="BRIDGE",
            inputs=[input_val.debugName()],
            outputs=[output_val.debugName()],
        )
        node.data.delete = True
        return node

    def get_shape(self, output: str) -> Tuple[int | None, ...]:
        if output not in self.shapes:
            shape_choices = list(self.shapes.keys())
            raise KeyError(f"No shape for output tensor of {self.op} '{output}'; choices are {shape_choices}")
        return self.shapes[output]

    def get_range(self, output: str) -> Tuple[float, float]:
        if output not in self.ranges:
            range_choices = list(self.ranges.keys())
            raise KeyError(f"No range for output tensor of {self.op} '{output}'; choices are {range_choices}")
        return self.ranges[output]


@dataclass
class VisSpec:
    width: int
    height: int


class PostprocessGraph(nx.DiGraph):
    """Defines a directed graph which is built from the Torch graph."""

    def add_postprocess_node(self, node: PostprocessNode) -> "PostprocessGraph":
        self.add_node(node.name, kind=NODE, node=node)
        for input_value in node.inputs:
            if not self.has_node(input_value):
                raise KeyError(f"Input for {node.op} node not found: {input_value}")
            self.add_edge(input_value, node.name)
        for output_value in node.outputs:
            self.add_node(output_value, kind=VALUE, node=node, value=output_value)
            self.add_edge(node.name, output_value)
        return self

    def remove_node_and_reconnect(self, node_name: str) -> None:
        """Removes a node and reconnects the graph around that node.

        Args:
            node_name: The name of the node to remove
        """

        node = self._node[node_name]
        assert node["kind"] == NODE

        # Gets the input and output values.
        input_value_names = [value_name for value_name, _ in self.in_edges(node_name)]
        output_value_names = [value_name for _, value_name in self.out_edges(node_name)]

        # For each user of an output, replace with all input values.
        for output_value_name in output_value_names:
            user_nodes = [user_node for _, user_node in self.out_edges(output_value_name)]
            for user_node in user_nodes:
                user_node_data = self.get_node_data(user_node)
                input_index = user_node_data.inputs.index(output_value_name)
                for input_value_name in input_value_names:
                    user_node_data.inputs.insert(input_index + 1, input_value_name)
                    self.add_edge(input_value_name, user_node)
                user_node_data.inputs.pop(input_index)
                self.remove_edge(output_value_name, user_node)
            self.remove_edge(node_name, output_value_name)
            self.remove_node(output_value_name)
        self.remove_node(node_name)

    def get_node_data(self, node_name: str) -> PostprocessNode:
        return self._node[node_name][NODE]

    def get_value_data(self, value_name: str) -> str:
        return self._node[value_name][VALUE]

    def gen_nodes(self, op: str | None = None) -> Iterator[Tuple[str, PostprocessNode]]:
        for node in list(nx.topological_sort(self)):
            if self._node[node]["kind"] == NODE:
                data = self.get_node_data(node)
                if op is None or data.op == op:
                    yield node, data

    def gen_values(self) -> Iterator[Tuple[str, PostprocessNode, str]]:
        for node in list(nx.topological_sort(self)):
            if self._node[node]["kind"] == VALUE:
                yield node, self.get_node_data(node), self.get_value_data(node)

    @property
    def num_nodes(self) -> int:
        return sum(1 for v in self._node.values() if v["kind"] == NODE)

    @property
    def num_values(self) -> int:
        return sum(1 for v in self._node.values() if v["kind"] == VALUE)

    def check_node_data(self) -> None:
        for node_name, node in self.gen_nodes():
            trg_inputs = {self.get_value_data(value_name) for value_name, _ in self.in_edges(node_name)}
            trg_outputs = {self.get_value_data(value_name) for _, value_name in self.out_edges(node_name)}
            assert set(node.inputs) == trg_inputs
            assert set(node.outputs) == trg_outputs

    def has_cycle(self) -> bool:
        try:
            nx.find_cycle(self, orientation="original")
            return True
        except nx.NetworkXNoCycle:
            return False

    def finalize(self) -> None:
        for node_name, node in list(self.gen_nodes()):
            if node.data.delete:
                self.remove_node_and_reconnect(node_name)
        self.check_node_data()
        assert not self.has_cycle()

    def visualize(self, save_path: str | Path) -> VisSpec:
        """Visualizes the graph and saves it to the provided path.

        Args:
            save_path: Where to save the generated image (extension should be
                something like `.png` or `.svg`)

        Returns:
            A spec describing the visualized graph
        """

        # Builds the graph to plot from the nodes of the current graph (mainly
        # just adapts the data to node labels).
        ops: DefaultDict[str, Set[int]] = defaultdict(set)
        labels: Dict[int, str] = {}
        node_ids: List[int] = []
        value_ids: List[int] = []
        graph_ids: Dict[str, int] = {}
        graph = nx.Graph()
        for _, node in self.gen_nodes():
            graph_ids[node.name] = (graph_node_id := len(graph))
            ops[node.op].add(graph_node_id)
            node_ids.append(graph_node_id)
            labels[graph_node_id] = f"{node.name}\n{node.op}"
            graph.add_node(graph_node_id)
            for value in node.inputs:
                graph.add_edge(graph_ids[value], graph_node_id)
            for value in node.outputs:
                graph_ids[value] = (graph_value_id := len(graph))
                ops["VALUE"].add(graph_value_id)
                value_ids.append(graph_value_id)
                label_strs: List[str] = [value]
                labels[graph_value_id] = "\n".join(label_strs)
                graph.add_edge(graph_node_id, graph_value_id)

        # Computes the positions of each node in the graph to ensure that all
        # connections are visible - basically, allocates columns to each
        # node so that if the node is used in the future, its column remains
        # empty.
        inds: LinkedList[str] = LinkedList()
        users: Dict[str, Set[str]] = {}
        height, width = 0, 0
        pos: Dict[int, Tuple[int, int]] = {}
        cols = inds.positions()
        for i, generation in enumerate(nx.topological_generations(self)):
            to_del: Set[str] = set()
            for node_name in generation:
                in_names = [in_name for in_name, _ in self.in_edges(node_name)]
                for in_name in in_names:
                    users[in_name].remove(node_name)
                    if len(users[in_name]) == 0:
                        to_del.add(in_name)
                users[node_name] = {edge[1] for edge in self.out_edges(node_name)}
                if in_names:
                    max_name = max((cols[in_name], in_name) for in_name in in_names)[1]
                    inds.extend(max_name, node_name)
                else:
                    inds.add(node_name)
            for del_name in to_del:
                inds.pop(del_name)
            cols = inds.positions()
            for node_name, col in cols.items():
                pos[graph_ids[node_name]] = (col, i)
            height, width = height + 1, max(width, len(cols))
        width_factor = 3
        pos = {k: (j * width_factor, height - i - 1) for k, (j, i) in pos.items()}

        plt.figure(figsize=(width * width_factor, height))

        node_options = {"node_size": 10}
        nx.draw_networkx_nodes(graph, pos, nodelist=node_ids, node_color="tab:red", **node_options)
        nx.draw_networkx_nodes(graph, pos, nodelist=value_ids, node_color="tab:blue", **node_options)

        edge_options = {"edge_color": "tab:grey"}
        nx.draw_networkx_edges(graph, pos, **edge_options)

        label_options = {
            "font_size": 15,
            "font_family": "monospace",
            "bbox": {"facecolor": "white", "edgecolor": "black", "boxstyle": "round,pad=0.2", "alpha": 0.5},
        }
        for _, op_graph_ids in ops.items():
            op_pos = {k: v for k, v in pos.items() if k in op_graph_ids}
            op_labels = {k: v for k, v in labels.items() if k in op_graph_ids}
            color_hex = hex(random.randint(16**5, 16**6 - 1))[2:]
            label_options["bbox"]["facecolor"] = f"#{color_hex}"  # type: ignore
            nx.draw_networkx_labels(graph, op_pos, labels=op_labels, **label_options)

        padding = 2

        plt.tight_layout()
        plt.axis("off")
        plt.xlim(-padding, (width - 1) * width_factor + padding)
        plt.ylim(-padding, height - 1 + padding)

        plt.savefig(save_path)

        return VisSpec(
            width=width,
            height=height,
        )

    def __str__(self) -> str:
        nodes_str = "\n".join(str(node) for _, node in self.gen_nodes())
        return f"Graph with {self.num_nodes} nodes and {self.num_values} values\n{nodes_str}"

    def save(self, path: str | Path) -> None:
        with open(path, "wb") as f:
            pickle.dump(self, f)

    @classmethod
    def load(cls, path: str | Path) -> "PostprocessGraph":
        with open(path, "rb") as f:
            return pickle.load(f)

    def get_spec(self) -> Spec:
        _, param_node = next(self.gen_nodes(op="prim::Param"))
        _, return_node = next(self.gen_nodes(op="prim::Return"))

        return Spec(
            inputs=[
                SpecTensor(
                    name=name,
                    shape=param_node.get_shape(name),
                )
                for name in param_node.outputs
            ],
            outputs=[
                SpecTensor(
                    name=name,
                    shape=return_node.get_shape(name),
                )
                for name in return_node.inputs
            ],
        )
