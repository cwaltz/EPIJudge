from typing import Optional

from list_node import ListNode
from test_framework import generic_test


def reverse_sublist_1(L: ListNode, start: int,
                      finish: int) -> Optional[ListNode]:
    if start == finish:
        return L

    old_head_pre = dummy_head = ListNode(next=L)  # old head's predecessor
    i = 1
    while i < start:
        old_head_pre = old_head_pre.next
        i += 1

    prev = old_head = old_head_pre.next
    curr = prev.next

    while i < finish:
        temp = curr.next
        curr.next = prev
        prev = curr
        curr = temp
        i += 1

    old_head_pre.next = prev
    old_head.next = curr
    return dummy_head.next


def reverse_sublist(head: Optional[ListNode], start: int, finish: int) -> Optional[ListNode]:

    dummy_head = pre_start = ListNode(0, head)  # pre_start is the predecessor of start node
    for _ in range(1, start):
        pre_start = pre_start.next

    # Reverses sublist.
    new_last = pre_start.next
    for _ in range(start, finish):
        temp = new_last.next
        new_last.next = temp.next
        temp.next = pre_start.next
        pre_start.next = temp
    return dummy_head.next


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('reverse_sublist.py',
                                       'reverse_sublist.tsv', reverse_sublist))
