from .torch_ops import *
from _typeshed import Incomplete
from torch import Tensor as Tensor

TORCH: Incomplete

def nucleus_sampling(logits: Tensor, nucleus_prob: float) -> Tensor: ...
