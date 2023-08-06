import re
from inspect import Traceback
from typing import Any, Iterable, List, Optional, Type, TypeVar

from torch._C import Node, Value

from infer.cpp.inference.inference import NodeException as BaseNodeException

T = TypeVar("T")


def render_node(node: Node) -> str:
    node_strs: List[str] = [f"{node.kind()} with {node.inputsSize()} input(s) and {node.outputsSize()} output(s)"]

    if node.sourceRange():
        match = re.search(r"File \"(.+?)\", line (\d+)", str(node.sourceRange()))
        if match:
            file, line_no = match.groups()
            node_strs += [f"  {file}:{line_no}"]

    return "\n".join(
        node_strs
        + [f"  -> {render_value(i, False)}" for i in node.inputs()]
        + [f"  <- {render_value(o, False)}" for o in node.outputs()]
    )


def render_value(value: Value, with_node: bool = True) -> str:
    value_str = f"{value.debugName()} of type {value.type()}"
    if with_node:
        return f"{value_str}\n\n{render_node(value.node())}"
    return value_str


class NodeException(BaseNodeException):
    """Exception on a particular node, set of nodes or set of values."""

    @classmethod
    def from_strs(cls, *msgs: str) -> "NodeException":
        return cls("\n\n".join(msgs))

    @classmethod
    def from_node(cls, msg: str, node: Node) -> "NodeException":
        return cls.from_strs(msg, render_node(node))

    @classmethod
    def from_nodes(cls, msg: str, nodes: Iterable[Node]) -> "NodeException":
        node_str = "\n\n".join(f"{i}. {render_node(node)}" for i, node in enumerate(nodes, 1))
        return cls.from_strs(msg, node_str)

    @classmethod
    def from_value(cls, msg: str, value: Value) -> "NodeException":
        return cls.from_strs(msg, render_value(value))

    @classmethod
    def from_values(cls, msg: str, values: Iterable[Value]) -> "NodeException":
        value_str = "\n\n".join(f"{i}. {render_value(value)}" for i, value in enumerate(values, 1))
        return cls.from_strs(msg, value_str)


class node_exception_handler:  # pylint: disable=invalid-name
    """Defines a context manager for grouping exceptions."""

    def __init__(self, max_exceptions: int = 10) -> None:
        self.exceptions: List[BaseNodeException] = []
        self.max_exceptions = max_exceptions

    def __enter__(self) -> "node_exception_handler":
        self.exceptions = []
        return self

    def __exit__(self, *args: Any, **kwargs: Any) -> bool:
        if self.exceptions:
            exc_strs = "\n\n".join(f"{i}. {exc}" for i, exc in enumerate(self.exceptions[: self.max_exceptions], 1))
            raise BaseNodeException(f"Found {len(self.exceptions)} exceptions:\n\n{exc_strs}")
        return True

    def single_handler(self) -> "single_exception_handler":
        return single_exception_handler(self)


class single_exception_handler:  # pylint: disable=invalid-name
    def __init__(self, base_handler: "node_exception_handler") -> None:
        self.base_handler = base_handler

    def __enter__(self) -> "single_exception_handler":
        return self

    def __exit__(self, etype: Optional[Type[Exception]], evalue: Optional[Exception], traceback: Traceback) -> bool:
        if evalue is not None:
            if not isinstance(evalue, BaseNodeException):
                raise evalue
            self.base_handler.exceptions.append(evalue)
        return True
