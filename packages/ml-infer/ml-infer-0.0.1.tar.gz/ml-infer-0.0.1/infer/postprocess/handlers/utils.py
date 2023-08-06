from __future__ import annotations

from typing import Optional, Tuple, TypeVar

T = TypeVar("T")


def rectify_dim(dim: Optional[int], rank: int) -> int:
    if dim is None:
        return 0
    return dim if dim >= 0 else rank + dim


def cast_item_not_none(i: T | None) -> T:
    assert i is not None
    return i


def cast_not_none(s: Tuple[T | None, ...]) -> Tuple[T, ...]:
    return tuple(cast_item_not_none(i) for i in s)
