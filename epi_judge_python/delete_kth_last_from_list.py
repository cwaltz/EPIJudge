from list_node import ListNode
from test_framework import generic_test


# Assumes L has at least k nodes, deletes the k-th last node in L.
def remove_kth_last(head: ListNode, k: int) -> ListNode | None:
    """
    #7.7

    Time complexity = O(n), where n is the length of the list.
    Space complexity = O(1)

    Test PASSED (306/306) [   1 ms]
    Average running time:    7 us
    Median running time:     1 us
    """
    dummy_head = pre = advanced = ListNode(0, head)
    for _ in range(k + 1):
        advanced = advanced.next

    while advanced:
        advanced = advanced.next
        pre = pre.next

    # predecessor's next node is kth last.
    pre.next = pre.next.next
    return dummy_head.next


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('delete_kth_last_from_list.py',
                                       'delete_kth_last_from_list.tsv',
                                       remove_kth_last))
