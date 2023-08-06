from typing import Any

from torch.jit import RecursiveScriptModule

from infer.quantization.observers import apply_to_observers

Observer = Any


def toggle_fake_quant(module: RecursiveScriptModule, enabled: bool) -> None:
    apply_to_observers(module, lambda observer: observer.set_fake_quantize_enabled(enabled))


def toggle_observer_enabled(module: RecursiveScriptModule, enabled: bool) -> None:
    apply_to_observers(module, lambda observer: observer.set_observer_enabled(enabled))


def toggle_track_quant_stats(module: RecursiveScriptModule, enabled: bool) -> None:
    apply_to_observers(module, lambda observer: observer.set_track_quant_stats(enabled))
