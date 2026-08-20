from list_node import ListNode
from test_framework import generic_test


def merge_two_sorted_lists(
        first: ListNode | None, second: ListNode | None) -> ListNode | None:
    """
    #7.1

    Time complexity = O(n + m), where n and m are the lengths of each of the two
        input lists.
    Space complexity = O(1)

    Test PASSED (501/501) [   1 ms]
    Average running time:    7 us
    Median running time:     2 us
    """
    # Creates a placeholder for the result.
    dummy_head = tail = ListNode()

    while first and second:
        if first.data < second.data:
            tail.next = first
            first = first.next
        else:  # second.data <= first.data
            tail.next = second
            second = second.next
        tail = tail.next

    # Appends the remaining nodes of first or second
    tail.next = first or second
    return dummy_head.next


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('sorted_lists_merge.py',
                                       'sorted_lists_merge.tsv',
                                       merge_two_sorted_lists))
