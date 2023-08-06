import random
from typing import Dict

import pytest

from infer.cpp.inference.inference import DisjointIntSet


@pytest.mark.parametrize("num_elems", [100])
@pytest.mark.parametrize("num_pairs", [50])
def test_disjoint_int_set(num_elems: int, num_pairs: int) -> None:
    """Tests that the underlying C++ DisjointSet implementation matches expected Python functionality.

    Args:
        num_elems: The number of elements to add to the set
        num_pairs: The number of elements which should share sets
    """

    values = list(range(num_elems))
    same_sets = [(random.randint(0, num_elems - 1), random.randint(0, num_elems - 1)) for _ in range(num_pairs)]

    # Builds the disjoint set.
    test_set = DisjointIntSet()
    for value in values:
        test_set += value
    for a, b in same_sets:
        test_set.join(a, b)
    sets = test_set.sets()

    # Checks some elements are not in the set.
    assert all(i not in test_set for i in (-1, num_elems))

    # Checks uniqueness.
    ref_set_ids: Dict[int, int] = test_set.set_ids()
    set_ids: Dict[int, int] = {}
    for s in sets:
        for si in s:
            assert si not in set_ids, "Found duplicate set item"
            assert si in ref_set_ids, "Item not in reference set ID dictionary"
            set_ids[si] = ref_set_ids[si]

    # Checks validity.
    for a, b in same_sets:
        assert set_ids[a] == set_ids[b], "Found incorrect set pair"
