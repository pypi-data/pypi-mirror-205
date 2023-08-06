"""Takes a preprocessed TorchScript graph and converts it to a NetworkX graph."""

from __future__ import annotations

import logging
from collections import defaultdict
from types import TracebackType
from typing import Any, DefaultDict, Dict, Iterator, List, Optional, Tuple

from torch._C import Block, Node, Value
from torch.jit import RecursiveScriptModule

from infer.cpp.inference.inference import Config, observer_name
from infer.postprocess.graph import (
    IfStatementData,
    LoopStatementData,
    PostprocessGraph,
    PostprocessNode,
)
from infer.postprocess.handler import HandlerData, register_handler

logger = logging.getLogger(__name__)


class NodeException(Exception):
    def __init__(
        self,
        *,
        node: Node | None = None,
        msg: str | Exception | None = None,
        sub_exceptions: List[NodeException] | None = None,
    ) -> None:
        self.excs: List[Tuple[Node, str | Exception]] = []
        if node is not None or msg is not None:
            assert node is not None and msg is not None, "Both `node` and `msg` must be provided"
            self.excs.append((node, msg))
        if sub_exceptions is not None:
            for sub_exception in sub_exceptions:
                self.excs.extend(sub_exception.excs)
        super().__init__(NodeException.exceptions_str(self.excs))

    @classmethod
    def exceptions_str(cls, excs: List[Tuple[Node, str | Exception]]) -> str:
        if len(excs) == 0:
            return "<Empty>"
        elif len(excs) == 1:
            return cls.exception_str(excs[0][0], excs[0][1])
        else:
            return "\n\n".join(f"{i}. {cls.exception_str(node, msg)}" for i, (node, msg) in enumerate(excs, 1))

    @classmethod
    def get_node_str(cls, node: Node) -> str:
        inputs = "\n".join(f" <- {value.debugName()}" for value in node.inputs())
        outputs = "\n".join(f" -> {value.debugName()}" for value in node.outputs())
        return f"{node.kind()}\n{inputs}\n{outputs}"

    @classmethod
    def last_traceback(cls, tb: TracebackType) -> TracebackType:
        while tb.tb_next is not None:
            tb = tb.tb_next
        return tb

    @classmethod
    def exception_str(cls, node: Node, msg: str | Exception) -> str:
        if isinstance(msg, Exception):
            if (tb := msg.__traceback__) is not None:
                tb = cls.last_traceback(tb)
                loc = f" ({tb.tb_frame.f_code.co_filename}:{tb.tb_lineno})"
            else:
                loc = ""
            msg = f"{msg.__class__.__name__}:  {' '.join(str(arg) for arg in msg.args)}{loc}"
        return f"{cls.get_node_str(node)}\n*** {msg.strip()} ***"

    @classmethod
    def throw_if(cls, sub_exceptions: List[NodeException]) -> None:
        if sub_exceptions:
            raise cls(sub_exceptions=sub_exceptions)


class _Generator:
    def __init__(self, model: RecursiveScriptModule, config: Optional[Config] = None) -> None:
        if model.training:
            logger.warning("Model is in training mode; this may cause unexpected or undesirable behavior")

        self.model = model
        self.config = Config() if config is None else config

        # Gets the observer from the model.
        if not hasattr(self.model, observer_name()):
            raise RuntimeError(f"Module is missing observer '{observer_name()}'; you need to run preprocessing first!")
        self.observer = getattr(self.model, observer_name())
        if not self.observer.get_has_been_called():
            raise RuntimeError("The observer hasn't been called yet; it must be called before graph generation")

        # Gets the TorchScript graph from the model.
        self.graph = getattr(self.model, self.config.export_func).graph

        # Defines the postprocess graph which is being built.
        self.output_graph = PostprocessGraph()

        # Contains the concrete evaluated values.
        self.concrete_values: Dict[str, Any] = {}

        self._call_counts: DefaultDict[str, int] = defaultdict(int)

        # Global dictionaries for tracking the shapes, ranges and name aliases.
        self.shapes: Dict[str, Tuple[int | None, ...]] = {}
        self.ranges: Dict[str, Tuple[float, float]] = {}
        self.names: Dict[str, Dict[str, Value]] = {}

    def get_data(self, node: Node) -> HandlerData:
        return HandlerData(
            node=node,
            concrete_values=self.concrete_values,
            shapes=self.shapes,
            ranges=self.ranges,
            names=self.names,
        )

    def gen_if(self, node: Node) -> Iterator[PostprocessNode]:
        exceptions: List[NodeException] = []

        cond_name = node.inputsAt(0).debugName()
        if cond_name in self.concrete_values:
            cond_value = self.concrete_values[cond_name]
            assert isinstance(cond_value, bool), f"Unexpected condition value type: {type(cond_value)}"
            true_block, false_block = node.blocks()
            block = true_block if cond_value else false_block
            try:
                yield from self.gen_block(block)
            except NodeException as e:
                exceptions.append(e)
            assert block.returnNode().inputsSize() == node.outputsSize()

            # Matches the block outputs with the node outputs.
            for block_out, node_out in zip(block.outputs(), node.outputs()):
                if block_out.debugName() in self.concrete_values:
                    self.concrete_values[node_out.debugName()] = self.concrete_values[block_out.debugName()]
                else:
                    output_node = self.get_data(node).default_node
                    output_node.data.delete = True
                    yield output_node
        else:
            true_block, false_block = node.blocks()
            if_node = self.get_data(node).default_node
            if_node.op = f"{if_node.op}::input"
            if_node.data.if_statement = IfStatementData(
                condition=cond_name,
                if_true_inputs=[i.debugName() for i in true_block.inputs()],
                if_true_outputs=[i.debugName() for i in true_block.outputs()],
                if_false_inputs=[i.debugName() for i in false_block.inputs()],
                if_false_outputs=[i.debugName() for i in false_block.outputs()],
            )
            yield if_node
            try:
                yield from self.gen_block(true_block)
                yield from self.gen_block(false_block)
            except NodeException as e:
                exceptions.append(e)

        NodeException.throw_if(exceptions)

    def gen_loop(self, node: Node) -> Iterator[PostprocessNode]:
        exceptions: List[NodeException] = []

        (block,) = node.blocks()

        block_inputs, block_outputs = list(block.inputs()), list(block.outputs())

        if all(v.debugName() in self.concrete_values for v in node.inputs()):
            # Copies input concrete values to loop input concrete values.
            for i in range(2, node.inputsSize()):
                in_name, loop_in_name = node.inputsAt(i).debugName(), block_inputs[i - 1].debugName()
                self.concrete_values[loop_in_name] = self.concrete_values[in_name]

            # This mimics PyTorch's loop execution form.
            max_trip_count = self.concrete_values[node.inputsAt(0).debugName()]
            condition = self.concrete_values[node.inputsAt(1).debugName()]
            i = 0
            while condition and i < max_trip_count:
                self.concrete_values[block_inputs[0].debugName()] = i
                try:
                    yield from self.gen_block(block)
                except Exception as e:
                    exceptions.append(NodeException(node=node, msg=e))
                condition = self.concrete_values[block_outputs[0].debugName()]
                i += 1

            # Copies loop output concrete values to output concrete values.
            for i in range(node.outputsSize()):
                loop_out_name, out_name = block_outputs[i + 1].debugName(), node.outputsAt(i).debugName()
                self.concrete_values[out_name] = self.concrete_values[loop_out_name]
        else:
            loop_node = self.get_data(node).default_node
            num_inputs, num_outputs = block.paramNode().outputsSize(), block.returnNode().inputsSize()
            loop_node.data.loop_statement = LoopStatementData(
                trip_count=node.inputsAt(0).debugName(),
                condition=node.inputsAt(1).debugName(),
                counter_input=block.paramNode().outputsAt(0).debugName(),
                counter_output=block.returnNode().inputsAt(0).debugName(),
                inputs=[block.paramNode().outputsAt(i).debugName() for i in range(1, num_inputs)],
                outputs=[block.returnNode().inputsAt(i).debugName() for i in range(1, num_outputs)],
            )
            yield loop_node

            try:
                yield from self.gen_block(block)
            except Exception as e:
                exceptions.append(NodeException(node=node, msg=e))

        NodeException.throw_if(exceptions)

    def gen_call_method(self, node: Node) -> Iterator[PostprocessNode]:
        exceptions: List[NodeException] = []

        model_name = node.inputsAt(0).debugName()
        func_name = node.s("name")
        call_signature = f"{model_name}_{func_name}"
        call_count = self._call_counts[call_signature]
        self._call_counts[call_signature] += 1
        submodel = self.concrete_values[model_name]
        subconfig = Config(self.config)
        subconfig.export_func = func_name
        generator = _Generator(submodel, subconfig)

        def mangle(name: str) -> str:
            # Mangling is required since the submodule is not unrolled, meaning
            # that TorchScript doesn't automatically handle name mangling.
            return f"{model_name}:{call_count}:{name}" if call_count > 0 else f"{model_name}:{name}"

        def mangle_values(vals: List[str]) -> List[str]:
            return [mangle(val) for val in vals]

        # Adds the concrete value corresponding to "self".
        for graph_input in generator.graph.inputs():
            if graph_input.debugName().startswith("self"):
                generator.concrete_values[graph_input.debugName()] = generator.model
                break

        block = generator.graph.block()

        # Bridge from function to block inputs.
        for i, block_input in enumerate(block.inputs()):
            func_input = node.inputsAt(i)
            if func_input.debugName() in self.concrete_values:
                generator.concrete_values[block_input.debugName()] = self.concrete_values[func_input.debugName()]
            else:
                bridge_node = PostprocessNode.get_bridge(func_input, block_input)
                bridge_node.outputs = mangle_values(bridge_node.outputs)
                bridge_node.data.delete = True
                yield bridge_node

        # Recursively adds all the nodes from the PyTorch graph.
        for block_node in block.nodes():
            try:
                for gen_node in generator.gen_node(block_node):
                    gen_node.inputs = mangle_values(gen_node.inputs)
                    gen_node.outputs = mangle_values(gen_node.outputs)
                    yield gen_node
            except Exception as e:
                exceptions.append(NodeException(node=block_node, msg=e))

        # Bridge from block to function outputs.
        for i, block_output in enumerate(block.outputs()):
            func_output = node.outputsAt(i)
            if block_output.debugName() in generator.concrete_values:
                self.concrete_values[node.output().debugName()] = block_output.debugName()
            else:
                bridge_node = PostprocessNode.get_bridge(block_output, func_output)
                bridge_node.inputs = mangle_values(bridge_node.inputs)
                bridge_node.data.delete = True
                yield bridge_node

        NodeException.throw_if(exceptions)

    def gen_node(self, node: Node) -> Iterator[PostprocessNode]:
        if node.kind() == "prim::If":
            yield from self.gen_if(node)
        elif node.kind() == "prim::Loop":
            yield from self.gen_loop(node)
        elif node.kind() == "prim::CallMethod":
            yield from self.gen_call_method(node)
        else:
            assert len(list(node.blocks())) == 0, "Found node with sub-blocks"
            data = self.get_data(node)
            handler = register_handler.lookup(data)
            opt_iter = handler(data)
            if opt_iter is not None:
                yield from opt_iter

    def gen_block(self, block: Block) -> Iterator[PostprocessNode]:
        exceptions: List[NodeException] = []

        if any(v.debugName() not in self.concrete_values for v in block.inputs()):
            try:
                yield from self.gen_node(block.paramNode())
            except Exception as e:
                exceptions.append(NodeException(node=block.paramNode(), msg=e))

        for node in block.nodes():
            try:
                yield from self.gen_node(node)
            except Exception as e:
                exceptions.append(NodeException(node=node, msg=e))

        if any(v.debugName() not in self.concrete_values for v in block.outputs()):
            try:
                yield from self.gen_node(block.returnNode())
            except Exception as e:
                exceptions.append(NodeException(node=block.returnNode(), msg=e))

        NodeException.throw_if(exceptions)

    def run(self) -> None:
        # Adds the concrete value corresponding to "self".
        for graph_input in self.graph.inputs():
            if graph_input.debugName().startswith("self"):
                self.concrete_values[graph_input.debugName()] = self.model
                break

        # Recursively adds all the nodes from the PyTorch graph.
        for node in list(self.gen_block(self.graph.block())):
            self.output_graph.add_postprocess_node(node)

        # Finalizes the NetworkX graph.
        self.output_graph.finalize()


def generate(model: RecursiveScriptModule, config: Optional[Config] = None) -> PostprocessGraph:
    """Defines the main postprocessing function.

    Args:
        model: The model to generate a postprocess graph for.
        config: The optional config, generally the one from preprocessing.

    Returns:
        The generated postprocess graph.
    """

    generator = _Generator(model, config)
    generator.run()
    return generator.output_graph
