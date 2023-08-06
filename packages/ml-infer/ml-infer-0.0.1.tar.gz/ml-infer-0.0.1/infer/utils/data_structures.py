from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Generic, List, TypeVar

K = TypeVar("K")
V = TypeVar("V")


@dataclass
class Node(Generic[K]):
    val: K
    next: Node[K]
    prev: Node[K]


class LinkedList(Generic[K]):
    """Defines a simple doubly-connected linked list.

    Operations:

    - add: Add an element in O(1)
    - extend: Add an element after a given element in O(1)
    - pop: Remove an element in O(1)
    - swap: Swaps an old value with a new value in O(1), equivalent to doing an
        `extend` with the new element then a `pop` the old element
    - empty: If the list is empty in O(1)
    - to_list: Converts the linked list to a regular list in O(N)
    - positions: Indices of each item in the linked list in O(N)

    This data structure was necessary for a particular graph visualization
    algorithm, probably isn't the best choice for other algorithms.
    """

    def __init__(self) -> None:
        self.lookup: Dict[K, Node[K]] = {}
        self.head: Node[K] | None = None

    def add(self, k: K) -> None:
        node = Node(val=k, next=None, prev=None)  # type: ignore
        self.lookup[k] = node
        if self.head is None:
            self.head = node
            self.head.next = self.head
            self.head.prev = self.head
        else:
            node.next = self.head
            node.prev = self.head.prev
            node.prev.next = node
            node.next.prev = node

    def extend(self, k: K, new_k: K) -> None:
        node = self.__get_node(k)
        new_node = Node(val=new_k, next=node.next, prev=node)
        node.next.prev = new_node
        node.next = new_node
        self.lookup[new_k] = new_node

    def pop(self, k: K) -> None:
        node = self.lookup.pop(k)
        if node == self.head:
            self.head = node.next
        if len(self.lookup) == 0:
            self.head = None
        else:
            node.prev.next = node.next
            node.next.prev = node.prev

    def swap(self, a: K, b: K) -> None:
        node = self.lookup.pop(a)
        node.val = b
        self.lookup[b] = node

    def empty(self) -> bool:
        return self.head is None

    def to_list(self) -> List[K]:
        items: List[K] = []
        if self.head is None:
            assert len(self) == 0
            return items
        node = self.head
        items.append(node.val)
        node = node.next
        while node != self.head:
            items.append(node.val)
            node = node.next
        assert len(self) == len(items)
        return items

    def positions(self) -> Dict[K, int]:
        return {k: i for i, k in enumerate(self.to_list())}

    def __get_node(self, k: K) -> Node[K]:
        node = self.lookup[k]
        assert node.val == k
        return node

    def __setitem__(self, k: K, v: K) -> None:
        self.swap(k, v)

    def __len__(self) -> int:
        return len(self.lookup)

    def __bool__(self) -> bool:
        return not self.empty()
