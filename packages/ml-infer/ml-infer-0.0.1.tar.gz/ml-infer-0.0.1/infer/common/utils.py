from typing import TYPE_CHECKING

from torch._C import DictType, ListType, TensorType, TupleType

if TYPE_CHECKING:
    from torch._C import JitType


def is_tensor_or_tensor_container(jit_type: "JitType") -> bool:
    if isinstance(jit_type, TensorType):
        return True
    if isinstance(jit_type, ListType):
        return is_tensor_or_tensor_container(jit_type.getElementType())
    if isinstance(jit_type, DictType):
        return is_tensor_or_tensor_container(jit_type.getValueType())
    if isinstance(jit_type, TupleType):
        return any(is_tensor_or_tensor_container(t) for t in jit_type.elements())
    return False


def is_tensor_container(jit_type: "JitType") -> bool:
    if isinstance(jit_type, ListType):
        return is_tensor_or_tensor_container(jit_type.getElementType())
    if isinstance(jit_type, DictType):
        return is_tensor_or_tensor_container(jit_type.getValueType())
    if isinstance(jit_type, TupleType):
        return any(is_tensor_or_tensor_container(t) for t in jit_type.elements())
    return False
