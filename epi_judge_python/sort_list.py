from typing import Any
from collections.abc import Callable

from list_node import ListNode
from sorted_lists_merge import merge_two_sorted_lists
from test_framework import generic_test


def _split_list(head: ListNode | None, step: int) -> ListNode | None:
    """
    Moves forward 'step' nodes, severs the list, and returns the next node.
    Returns None if the list is shorter than 'step'.
    """
    if not head:
        return None

    # Move forward step - 1 times to reach the end of this chunk
    for _ in range(step - 1):
        if not head.next:
            break
        head = head.next

    # Sever the link and return the start of the next chunk
    right_head = head.next
    head.next = None
    return right_head


def _merge_lists(
        l1: ListNode | None,
        l2: ListNode | None,
        key: Callable[[Any], Any],
        reverse: bool
) -> tuple[ListNode, ListNode]:
    """
    Merges two sorted lists and returns the (head, tail) of the merged list.
    """
    dummy = tail = ListNode(None)  # type: ignore

    while l1 and l2:
        val1, val2 = key(l1.data), key(l2.data)
        condition = (val1 > val2) if reverse else (val1 < val2)

        if condition:
            tail.next = l1
            l1 = l1.next
        else:
            tail.next = l2
            l2 = l2.next
        tail = tail.next

    # Append any remaining nodes
    tail.next = l1 or l2

    # Advance tail pointer to the very end of the newly merged segment
    while tail.next:
        tail = tail.next

    return dummy.next, tail  # type: ignore


def bottom_up_merge_sort(
        head: ListNode | None,
        key: Callable[[Any], Any] = lambda x: x,
        reverse: bool = False
) -> ListNode | None:
    """
    Iterative merge sort for a linked list.
    Time Complexity: O(N log N)
    Space Complexity: O(1)

    Test PASSED (209/209) [  22 ms]
    Average running time:  473 us
    Median running time:    24 us
    """
    if not head or not head.next:
        return head

    # 1. Get the length of the list
    length = 0
    curr: ListNode | None = head
    while curr:
        length += 1
        curr = curr.next

    # 2. Bottom-up iterative merge
    dummy = ListNode(None)  # type: ignore
    dummy.next = head

    step = 1
    while step < length:
        prev = dummy
        curr = dummy.next

        while curr:
            left = curr

            # Extract the right sublist of size 'step'
            right = _split_list(left, step)

            # Extract the remainder of the list for the next iteration
            curr = _split_list(right, step)

            # Merge left and right segments
            merged_head, merged_tail = _merge_lists(left, right, key, reverse)

            # Reattach the merged segment to our main list
            prev.next = merged_head
            prev = merged_tail

        step *= 2

    return dummy.next


def stable_sort_list(head: ListNode) -> ListNode | None:
    """
    Time complexity = O(n log n) for classic merge sort
    Space complexity = O(log n) on function call stack

    Test PASSED (209/209) [  13 ms]
    Average running time:  271 us
    Median running time:    13 us
    """

    # Base cases: head is empty or a single node, nothing to do.
    if head is None or head.next is None:
        return head

    # Find the midpoint of head using a slow and a fast pointer.
    pre_slow, slow, fast = None, head, head
    while fast and fast.next:
        pre_slow = slow
        fast, slow = fast.next.next, slow.next

    if pre_slow:
        pre_slow.next = None  # Splits the list into two equal-sized lists.

    return merge_two_sorted_lists(stable_sort_list(head),
                                  stable_sort_list(slow))


def insertion_sort_list(head: ListNode) -> ListNode | None:
    """
    Time complexity = O(n ** 2)
    Space complexity = O(1)

    Test PASSED (209/209) [ 510 ms]
    Average running time:    7 ms
    Median running time:     6 us
    """

    dummy_head = ListNode(0, head)
    # The sublist consisting of nodes up to and including iter is sorted in
    # increasing order. We need to ensure that after we nove to head.next this
    # property continues to hold. We do this by swapping head.next with its
    # predecessors in the list till it's in the right place.
    while head and head.next:
        if head.data > head.next.data:
            target, pre = head.next, dummy_head
            while pre.next.data < target.data:
                pre = pre.next
            temp, pre.next, head.next = pre.next, target, target.next
            target.next = temp
        else:
            head = head.next
    return dummy_head.next


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('sort_list.py',
                                       'sort_list.tsv',
                                       bottom_up_merge_sort))
