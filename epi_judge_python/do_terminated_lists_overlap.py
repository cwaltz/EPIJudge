import functools

from list_node import ListNode
from test_framework import generic_test
from test_framework.test_failure import TestFailure
from test_framework.test_utils import enable_executor_hook


def list_length(head: ListNode) -> int:
    length = 0
    while head:
        length += 1
        head = head.next
    return length


def overlapping_no_cycle_lists(first: ListNode, second: ListNode) -> (
        ListNode | None):
    """
    #7.4

    Time complexity = O(n + m), where n and m are the lengths of each of the
        two input lists.
    Space complexity = O(1)

    Test PASSED (106/106) [  11 ms]
    Average running time:  168 us
    Median running time:     5 us
    """
    if not first or not second:
        return None

    first_length, second_length = list_length(first), list_length(second)

    if first_length < second_length:
        first, second = second, first  # first is the longer list

    # Advances the longer list to get equal length lists.
    for _ in range(abs(first_length - second_length)):
        first = first.next

    while first is not second:
        first, second = first.next, second.next

    return first  # None implies there is no overlap between first and second.


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
