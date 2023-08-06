from typing import Any, Callable, Dict, cast

from torch.jit import RecursiveScriptModule

from infer.cpp.inference import observer_name

Observer = Any


def get_observers(module: RecursiveScriptModule) -> Dict[str, Observer]:
    observers = {"": getattr(module, observer_name())} if hasattr(module, observer_name()) else {}
    for name, submodule in module.named_children():
        for child_name, observer in get_observers(cast(RecursiveScriptModule, submodule)).items():
            observers[f"{name}.{child_name}" if child_name else name] = observer
    return observers


def apply_to_observers(module: RecursiveScriptModule, func: Callable[[Observer], None]) -> None:
    for observer in get_observers(module).values():
        func(observer)
