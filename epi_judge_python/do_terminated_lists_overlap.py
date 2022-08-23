import functools
from typing import Optional

from list_node import ListNode
from test_framework import generic_test
from test_framework.test_failure import TestFailure
from test_framework.test_utils import enable_executor_hook


def overlapping_no_cycle_lists(l0: ListNode, l1: ListNode) -> Optional[ListNode]:
    """
    #7.4

    Time complexity = O(n + m), where n and m are the lengths of each of the two input lists.
    Space complexity = O(1)

    Test PASSED (106/106) [  14 ms]
    Average running time:  230 us
    Median running time:     6 us
    """
    if not l0 or not l1:
        return None

    def length(head: ListNode) -> int:
        length = 0
        while head:
            length += 1
            head = head.next
        return length

    length0, length1 = length(l0), length(l1)

    if length0 < length1:
        l0, l1 = l1, l0  # l0 is the longer list
    # Advances the longer list to get equal length lists.
    for _ in range(abs(length0 - length1)):
        l0 = l0.next

    while l0 is not l1:
        l0, l1 = l0.next, l1.next
    return l0  # None implies there is no overlap between l0 and l1.


@enable_executor_hook
def overlapping_no_cycle_lists_wrapper(executor, l0, l1, common):
    if common:
        if l0:
            i = l0
            while i.next:
                i = i.next
            i.next = common
        else:
            l0 = common

        if l1:
            i = l1
            while i.next:
                i = i.next
            i.next = common
        else:
            l1 = common

    result = executor.run(functools.partial(overlapping_no_cycle_lists, l0,
                                            l1))

    if result != common:
        raise TestFailure('Invalid result')


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('do_terminated_lists_overlap.py',
                                       'do_terminated_lists_overlap.tsv',
                                       overlapping_no_cycle_lists_wrapper))
