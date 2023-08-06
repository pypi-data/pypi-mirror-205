from typing import Dict, List, Tuple

from torch.jit import RecursiveScriptModule

from infer.quantization.observers import get_observers


def get_quant_stats(module: RecursiveScriptModule) -> Dict[str, List[Tuple[float, float]]]:
    quant_stats: Dict[str, List[Tuple[float, float]]] = {}
    for name, observer in get_observers(module).items():
        obs_stats: List[Tuple[float, float]] = []
        for tensor_id in range(observer.num_tensors()):
            sqnr = observer.get_mean_sqnr(tensor_id)
            l1_err = observer.get_mean_l1_err(tensor_id)
            obs_stats.append((sqnr, l1_err))
        quant_stats[name] = obs_stats
    return quant_stats
