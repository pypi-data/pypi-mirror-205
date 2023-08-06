# pylint: disable=too-many-public-methods

from __future__ import annotations

import itertools
from dataclasses import dataclass
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Iterator,
    List,
    Optional,
    Tuple,
    TypeVar,
    cast,
)

from torch import Tensor
from torch._C import Node, Value

from infer.postprocess.graph import NewTensorData, PostprocessNode

if TYPE_CHECKING:
    from infer.cpp.inference import Observer

T = TypeVar("T")


def maybe_get_observer_value(value: Value) -> Value | None:
    if value.node().kind() == "inference::observe":
        return value
    if len(uses := value.uses()) != 1:
        return None
    user = uses[0].user
    if user.kind() != "inference::observe":
        return None
    return user.output()


def maybe_get_attr_recursive(value: Value, concrete_values: Dict[str, Any]) -> Any | None:
    if value.debugName() in concrete_values:
        return concrete_values[value.debugName()]
    if value.node().kind() != "prim::GetAttr":
        return None
    parent = maybe_get_attr_recursive(value.node().inputsAt(0), concrete_values)
    if parent is None:
        return None
    obj = getattr(parent, value.node().s("name"))
    concrete_values[value.debugName()] = obj
    return obj


def maybe_get_observer(value: Value, concrete_values: Dict[str, Any]) -> Tuple["Observer" | None, Node | None]:
    obs_value = maybe_get_observer_value(value)
    if obs_value is None:
        return None, obs_value
    obs_node = obs_value.node()
    obs = maybe_get_attr_recursive(obs_node.inputsAt(0), concrete_values)
    return cast("Observer | None", obs), obs_node


def maybe_get_shape(value: Value, concrete_values: Dict[str, Any]) -> Tuple[int | None, ...] | None:
    obs, obs_node = maybe_get_observer(value, concrete_values)
    if obs is None or obs_node is None:
        return None
    val_shape = obs.get_shape(obs_node.i("shape"))
    return None if val_shape is None else tuple(val_shape)


def maybe_get_range(value: Value, concrete_values: Dict[str, Any]) -> Tuple[float, float] | None:
    obs, obs_node = maybe_get_observer(value, concrete_values)
    if obs is None or obs_node is None:
        return None
    val_range = obs.get_range(obs_node.i("shape"))
    return val_range


def check_not_none(value: T | None) -> T:
    assert value is not None
    return value


@dataclass
class HandlerData:
    node: Node
    concrete_values: Dict[str, Any]
    shapes: Dict[str, Tuple[int | None, ...]]
    ranges: Dict[str, Tuple[float, float]]
    names: Dict[str, Dict[str, Value]]

    @property
    def kind(self) -> str:
        return self.node.kind()

    @property
    def num_inputs(self) -> int:
        return self.node.inputsSize()

    @property
    def num_outputs(self) -> int:
        return self.node.outputsSize()

    @property
    def concrete(self) -> Optional[bool]:
        definitely_concrete = all(value.debugName() in self.concrete_values for value in self.node.inputs())
        if definitely_concrete:
            return True
        definitely_not_concrete = all(value.debugName() not in self.concrete_values for value in self.node.inputs())
        if definitely_not_concrete:
            return False
        return None

    @property
    def implicit_inds(self) -> Tuple[int, ...]:
        return tuple(i for i, value in enumerate(self.node.inputs()) if value.debugName() not in self.concrete_values)

    @property
    def input_name(self) -> str:
        return self.node.input().debugName()

    @property
    def input_names(self) -> List[str]:
        return [value.debugName() for value in self.node.inputs()]

    @property
    def output_name(self) -> str:
        return self.node.output().debugName()

    @property
    def output_names(self) -> List[str]:
        return [value.debugName() for value in self.node.outputs()]

    def concrete_shape(self, key: str) -> Tuple[int, ...]:
        return tuple(check_not_none(i) for i in self.shapes[key])

    def input(self, i: int) -> Value:
        return self.node.inputsAt(i)

    def output(self, i: int) -> Value:
        return self.node.outputsAt(i)

    def input_shape(self, i: int = 0) -> Tuple[int | None, ...]:
        input_val = self.input(i)
        if (input_shape := maybe_get_shape(input_val, self.concrete_values)) is None:
            raise ValueError(f"Input {i} shape is missing")
        return input_shape

    def input_shapes(self) -> Dict[str, Tuple[int | None, ...]]:
        shapes = {value.debugName(): maybe_get_shape(value, self.concrete_values) for value in self.node.inputs()}
        return {k: v for k, v in shapes.items() if v is not None}

    def output_shape(self, i: int = 0) -> Tuple[int | None, ...]:
        output_val = self.output(i)
        if (output_shape := maybe_get_shape(output_val, self.concrete_values)) is None:
            raise ValueError(f"Output {i} shape is missing")
        return output_shape

    def output_shapes(self) -> Dict[str, Tuple[int | None, ...]]:
        shapes = {value.debugName(): maybe_get_shape(value, self.concrete_values) for value in self.node.outputs()}
        return {k: v for k, v in shapes.items() if v is not None}

    def input_range(self, i: int = 0) -> Tuple[float, float]:
        input_val = self.input(i)
        if (input_range := maybe_get_range(input_val, self.concrete_values)) is None:
            raise ValueError(f"Input {i} shape is missing")
        return input_range

    def input_ranges(self) -> Dict[str, Tuple[float, float]]:
        ranges = {value.debugName(): maybe_get_range(value, self.concrete_values) for value in self.node.inputs()}
        return {k: v for k, v in ranges.items() if v is not None}

    def output_range(self, i: int = 0) -> Tuple[float, float]:
        output_val = self.output(i)
        if (output_range := maybe_get_range(output_val, self.concrete_values)) is None:
            raise ValueError(f"Output {i} shape is missing")
        return output_range

    def output_ranges(self) -> Dict[str, Tuple[float, float]]:
        ranges = {value.debugName(): maybe_get_range(value, self.concrete_values) for value in self.node.outputs()}
        return {k: v for k, v in ranges.items() if v is not None}

    @property
    def default_node(self) -> PostprocessNode:
        n = self.node

        node = PostprocessNode(
            op=n.kind(),
            inputs=list(filter(lambda i: i not in self.concrete_values, (v.debugName() for v in n.inputs()))),
            outputs=list(filter(lambda i: i not in self.concrete_values, (v.debugName() for v in n.outputs()))),
            shapes=self.shapes,
            ranges=self.ranges,
        )

        # Adds output shapes and ranges to global dictionaries.
        self.shapes.update(self.input_shapes())
        self.shapes.update(self.output_shapes())
        self.ranges.update(self.input_ranges())
        self.ranges.update(self.output_ranges())

        return node

    def new_tensor_node(self, name: str, value: Tensor) -> PostprocessNode:
        node = PostprocessNode(
            op="inference::new_tensor",
            inputs=[],
            outputs=[name],
            shapes=self.shapes,
            ranges=self.ranges,
        )

        node.data.new_tensor = NewTensorData(value=value)

        # Get range and shape for the tensor.
        tensor_shape = tuple(value.shape)
        if value.is_floating_point():
            tensor_range = (value.quantile(1 / 256).item(), value.quantile(255 / 256).item())
        else:
            min_val, max_val = value.aminmax()
            tensor_range = (min_val.item(), max_val.item())

        # Adds output shapes and ranges to global dictionaries.
        self.shapes[name] = tensor_shape
        self.ranges[name] = tensor_range

        return node


Handler = Callable[[HandlerData], Optional[Iterator[PostprocessNode]]]


@dataclass(frozen=True)
class NodeKey:
    kind: str
    num_inputs: Optional[int] = None
    num_outputs: Optional[int] = None
    concrete: Optional[bool] = None
    implicit_inds: Optional[Tuple[int, ...]] = None


class register_handler:  # pylint: disable=invalid-name
    REGISTRY: Dict[NodeKey, Handler] = {}

    def __init__(
        self,
        kind: str,
        *,
        num_inputs: Optional[int] = None,
        num_outputs: Optional[int] = None,
        concrete: Optional[bool] = None,
        implicit_inds: Optional[Tuple[int, ...]] = None,
    ) -> None:
        self.key = NodeKey(
            kind=kind,
            num_inputs=num_inputs,
            num_outputs=num_outputs,
            concrete=concrete,
            implicit_inds=implicit_inds,
        )

    def __call__(self, handler: Handler) -> Handler:
        self.REGISTRY[self.key] = handler
        return handler

    @classmethod
    def gen_keys(cls, data: HandlerData) -> Iterator[NodeKey]:
        for num_inputs, num_outputs, concrete, implicit_inds in itertools.product(
            (data.num_inputs, None),
            (data.num_outputs, None),
            (data.concrete, None),
            (data.implicit_inds, None),
        ):
            yield NodeKey(
                kind=data.kind,
                num_inputs=num_inputs,
                num_outputs=num_outputs,
                concrete=concrete,
                implicit_inds=implicit_inds,
            )

    @classmethod
    def lookup(cls, data: HandlerData) -> Handler:
        """Gets the function to handle the particular node.

        Args:
            data: The handler data to lookup in the registry

        Returns:
            The handler function for the node

        Raises:
            KeyError: If there isn't a handler implemented for the function
        """

        for key in cls.gen_keys(data):
            if key in cls.REGISTRY:
                return cls.REGISTRY[key]
        raise KeyError(f"Handler not found for {next(cls.gen_keys(data))}\n\n{data.node}")


# Imports all the handler implementations here, so that the registry is populated.
from .handlers import *  # noqa, pylint: disable=wildcard-import,wrong-import-position,unused-wildcard-import
