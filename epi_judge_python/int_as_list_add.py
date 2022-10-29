from typing import Optional

from list_node import ListNode
from test_framework import generic_test


def add_two_numbers(l1: ListNode, l2: ListNode) -> Optional[ListNode]:
    """
    #7.13

    Time complexity = O(max(n1, n2))), n1 = len(l1), n2 = len(l2)
    Space complexity = O(1) except for the result linked list

    Test PASSED (2002/2002) [ 509 us]
    Average running time:   58 us
    Median running time:    23 us
    """
    curr = dummy_head = ListNode()
    carry = 0
    while l1 or l2 or carry:
        total = carry + (l1.data if l1 else 0) + (l2.data if l2 else 0)
        l1 = l1.next if l1 else None
        l2 = l2.next if l2 else None
        curr.next = ListNode(total % 10)
        curr = curr.next
        carry = total // 10
    return dummy_head.next


def add_two_numbers_faster(l1: ListNode, l2: ListNode) -> Optional[ListNode]:
    """
    Test PASSED (2002/2002) [ 496 us]
    Average running time:   33 us
    Median running time:    10 us
    """
    dummy_head = curr = ListNode()
    carry = 0
    while l1 and l2:
        carry, digit = divmod(l1.data + l2.data + carry, 10)
        curr.next = ListNode(digit)
        l1, l2, curr = l1.next, l2.next, curr.next
    remaining = l1 or l2
    while carry and remaining:
        carry, digit = divmod(remaining.data + carry, 10)
        curr.next = ListNode(digit)
        remaining, curr = remaining.next, curr.next
    if carry:
        curr.next = ListNode(carry)
    if remaining:
        curr.next = remaining
    return dummy_head.next


def add_two_numbers_fastest(l1: ListNode, l2: ListNode) -> Optional[ListNode]:
    """
    Test PASSED (2002/2002) [ 477 us]
    Average running time:   32 us
    Median running time:    10 us
    """
    dummy_head = curr = ListNode()
    carry = 0
    while l1 and l2:
        total, carry = l1.data + l2.data + carry, 0
        if total > 9:
            total, carry = total - 10, 1
        curr.next = ListNode(total)
        l1, l2, curr = l1.next, l2.next, curr.next
    remaining = l1 or l2
    while carry and remaining:
        total, carry = remaining.data + carry, 0
        if total > 9:
            total, carry = total - 10, 1
        curr.next = ListNode(total)
        remaining, curr = remaining.next, curr.next
    if carry:
        curr.next = ListNode(carry)
    if remaining:
        curr.next = remaining
    return dummy_head.next


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('int_as_list_add.py',
                                       'int_as_list_add.tsv', add_two_numbers))
