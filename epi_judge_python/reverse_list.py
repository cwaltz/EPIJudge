from list_node import ListNode
from test_framework import generic_test


def reverse_list(head: ListNode) -> ListNode:
    dummy = ListNode(0)
    while head:
        dummy.next, head.next, head = head, dummy.next, head.next
    return dummy.next


def reverse_list_recursive(head: ListNode) -> ListNode:
    if not (head and head.next):
        return head

    new_head = reverse_list_recursive(head.next)
    head.next.next = head
    head.next = None
    return new_head


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('reverse_list.py', 'reverse_list.tsv',
                                       reverse_list))
