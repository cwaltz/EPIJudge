from list_node import ListNode
from test_framework import generic_test


def reverse_sublist(node: ListNode, start: int,
                    finish: int) -> ListNode | None:
    """
    #7.2

    Time complexity = O(f), the time complexity is dominated by the search for
        the fth node.
    Space complexity = O(1)

    Test PASSED (210/210) [   1 ms]
    Average running time:    9 us
    Median running time:     1 us
    """
    dummy_head = sublist_head = ListNode(0, node)
    for _ in range(1, start):
        sublist_head = sublist_head.next  # Dummy head of the sublist

    # Reverses sublist.
    sublist_iter = sublist_head.next  # Old head as well as new tail of sublist
    for _ in range(finish - start):
        temp = sublist_iter.next
        sublist_iter.next, temp.next, sublist_head.next = (temp.next,
                                                           sublist_head.next,
                                                           temp)
    return dummy_head.next


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main(
            'reverse_sublist.py',
            'reverse_sublist.tsv', reverse_sublist))
