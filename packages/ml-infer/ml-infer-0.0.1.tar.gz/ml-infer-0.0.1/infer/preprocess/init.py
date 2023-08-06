from __future__ import annotations

import logging
import warnings
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Sequence,
    Set,
    Tuple,
    Union,
    cast,
)

import torch
from torch import Tensor, nn
from torch.jit import RecursiveScriptModule
from torch.jit._recursive import wrap_cpp_module

from infer.cpp.inference import (
    Config,
    apply_all_passes,
    get_implicit_tensors,
    insert_all_observers,
    insert_observers,
    quantize_props,
)

logger = logging.getLogger(__name__)

ExamplesType = Union[Sequence[Tuple], Dict[Callable, Sequence[Tuple]], None]

# These node kinds should have been removed from the graph.
ILLEGAL_KINDS: Set[str] = {
    "prim::CallMethod",
    "prim::CallFunction",
}


def get_outputs(model: nn.Module | RecursiveScriptModule, example_inputs: ExamplesType) -> ExamplesType:
    if example_inputs is None:
        return None
    if isinstance(example_inputs, Sequence):
        return [model(*i) for i in example_inputs]
    if isinstance(example_inputs, Dict):
        return {k: model(*v) for k, v in example_inputs.items()}
    raise RuntimeError("Unexpected example inputs type")


def is_match(out: Any, ref: Any) -> bool:
    if ref is None:
        return out is None
    if isinstance(ref, Sequence):
        if isinstance(out, Sequence):
            return all(is_match(a, b) for a, b in zip(out, ref))
        return False
    if isinstance(ref, tuple):
        if isinstance(out, tuple):
            return all(is_match(a, b) for a, b in zip(out, ref))
        return False
    if isinstance(ref, Dict):
        if isinstance(out, Dict):
            return all(is_match(av, bv) for (_, av), (_, bv) in zip(out.items(), ref.items()))
        return False
    if isinstance(ref, Tensor):
        if isinstance(out, Tensor):
            return (ref - out).abs().max().item() < 1e-9
        return False
    return ref == out


def run_preprocess_checks(model: RecursiveScriptModule, config: Optional[Config] = None) -> None:
    """Runs preprocessing checks on the model, to ensure it is exportable.

    Args:
        model: The model to check
        config: The preprocessing ocnfig to check

    Raises:
        ValueError: If the model fails preprocessing checks
    """

    if config is None:
        config = Config()

    try:
        implicit_tensors_map = get_implicit_tensors(model._c, config)
        if not implicit_tensors_map:
            raise ValueError("Model does not have any implicit tensors!")

    except Exception as e:
        raise ValueError("Model failed preprocessing checks") from e


def _make_props_constant(model: nn.Module) -> None:
    for submodel in model.children():
        _make_props_constant(submodel)

    # By default, class constants are not added to the TorchScript graph.
    # This automatically adds any of the quantize properties as constants.
    prop_constants: List[str] = [prop for prop in quantize_props() if hasattr(model, prop)]
    if prop_constants:
        if hasattr(model, "__constants__"):
            constants = list(cast(List[str], model.__constants__))
            constants_set = set(constants)
            setattr(model, "__constants__", constants + [p for p in prop_constants if p not in constants_set])
        else:
            setattr(model, "__constants__", prop_constants)


def preprocess_(
    model: nn.Module,
    example_inputs: ExamplesType = None,
    config: Optional[Config] = None,
    *,
    check_scripted: bool = False,
    check_against_self: bool = False,
    separate_passes: bool = False,
) -> RecursiveScriptModule:
    """Initializes the model to be exported.

    Args:
        model: The module to convert to TorchScript and export
        example_inputs: Optional example inputs which are used to validate that
            the preprocessing steps don't change the model's control flow
        config: Optional config to provide
        check_scripted: If set, check that the scripted module outputs match
            the unscripted module outputs (basically, checking for errors in
            some core TorchScript code)
        check_against_self: If set, check the outputs of the base model against
            itself, to check for differences due to stochastic behavior
        separate_passes: If set, separates the graph manipulation passes from
            the pass to insert observers. Note that this will not work for
            nested quantization modules

    Returns:
        The preprocessed model

    Raises:
        RuntimeError: If the model outputs don't match at some stage
    """

    if config is None:
        config = Config()

    _make_props_constant(model)

    if check_against_self and not is_match(get_outputs(model, example_inputs), get_outputs(model, example_inputs)):
        raise RuntimeError("The model exhibits stochastic behavior (same inputs generate different outputs)")

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        scripted_model = torch.jit.script(model, example_inputs=example_inputs)  # type: ignore

    # If an example input is provided, runs an inference step to check the
    # output after applying preprocessing passes against the output before
    # applying preprocessing passes (as a sanity check).
    pre_outputs = get_outputs(scripted_model, example_inputs)

    if check_scripted and not is_match(get_outputs(model, example_inputs=example_inputs), pre_outputs):
        raise RuntimeError("TorchScript outputs don't match vanilla PyTorch outputs")

    if separate_passes:
        # Applies initial passes to the model.
        scripted_model = wrap_cpp_module(apply_all_passes(scripted_model._c, config, True))
        if not is_match(get_outputs(scripted_model, example_inputs), pre_outputs):
            raise RuntimeError("Model outputs don't match after applying passes")

        # Adds quantization observers to the model.
        scripted_model = wrap_cpp_module(insert_observers(scripted_model._c, config, True))
        if not is_match(get_outputs(scripted_model, example_inputs), pre_outputs):
            raise RuntimeError("Model outputs don't match after adding quant observers")

    else:
        # Adds quantization observers to the model.
        scripted_model = wrap_cpp_module(insert_all_observers(scripted_model._c, config, True))
        if not is_match(get_outputs(scripted_model, example_inputs), pre_outputs):
            raise RuntimeError("Model outputs don't match after adding quant observers")

    return scripted_model
