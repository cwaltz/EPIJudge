"""
from typing import Any
from collections.abc import Callable


class ListNode[T]:
    def __init__(self, data: T, next: "ListNode[T] | None" = None):
        self.data = data
        self.next = next


def merge_two_sorted_lists[T](
        first: ListNode[T] | None,
        second: ListNode[T] | None,
        key: Callable[[T], Any] = lambda x: x,
        reverse: bool = False
) -> ListNode[T] | None:
    # Placeholder node; data is None, so we ignore the type check here
    dummy_head = tail = ListNode[Any](None)  # type: ignore

    while first and second:
        # Evaluate keys
        val1, val2 = key(first.data), key(second.data)

        # Determine sorting condition based on reverse flag
        condition = (val1 > val2) if reverse else (val1 < val2)

        if condition:
            tail.next = first
            first = first.next
        else:
            tail.next = second
            second = second.next
        tail = tail.next

    tail.next = first or second
    return dummy_head.next
"""

