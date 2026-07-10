from list_node import ListNode
from test_framework import generic_test


def even_odd_merge_extensible(head: ListNode) -> ListNode | None:
    """
    #7.10

    Time complexity = O(n + k)
    Space complexity = O(k)

    Test PASSED (1015/1015) [   9 ms]
    Average running time:   19 us
    Median running time:     4 us
    """
    return k_way_alternate_merge(head, 2)


def k_way_alternate_merge(head: ListNode | None, k: int) -> ListNode | None:
    # Edge case: no list to process, or k is 1 (meaning no split needed)
    if not head or k <= 1:
        return head

    # 1. Create an array of k dummy heads and a matching array of tails
    dummies = [ListNode() for _ in range(k)]
    tails = [dummy for dummy in dummies]

    # 2. Route each node into its respective group
    turn = 0
    while head:
        tails[turn].next = head
        head = head.next
        tails[turn] = tails[turn].next
        turn = (turn + 1) % k  # Move to the next group, wrapping around to 0

    # 3. Terminate the final sub-list
    # (all other tails are overwritten during stitching)
    tails[-1].next = None

    # 4. Stitch the groups together sequentially
    for i in range(k - 1):
        # Attach the end of the current group to the start of the next group
        tails[i].next = dummies[i + 1].next

    # Return the true head of the first group
    return dummies[0].next


def even_odd_merge_epi(head: ListNode) -> ListNode | None:
    """
    Test PASSED (1015/1015) [   8 ms]
    Average running time:   16 us
    Median running time:     4 us
    """
    if not head:
        return head

    dummies = [ListNode() for _ in range(2)]
    tails = [dummy for dummy in dummies]

    turn = 0
    while head:
        tails[turn].next = head
        head = head.next
        tails[turn] = tails[turn].next
        turn ^= 1

    tails[1].next = None
    # Always terminate your sub-lists (tails[1].next = None) BEFORE you stitch
    # them into other lists (tails[0].next = dummies[1].next) to avoid cycles.

    tails[0].next = dummies[1].next
    return dummies[0].next


def even_odd_merge_non_extensible(head: ListNode) -> ListNode | None:
    """
    Test PASSED (1015/1015) [   4 ms]
    Average running time:    8 us
    Median running time:     2 us
    """
    if not head or not head.next or not head.next.next:
        # If there are less than 3 nodes, there is nothing to do
        return head

    dummy_even_head = ListNode(0, head)
    even, odd = head, head.next
    dummy_odd_head = ListNode(0, odd)

    while even.next:
        even.next = odd.next

        if odd.next:
            even = even.next
            odd.next = even.next
            odd = odd.next
        else:
            break

    even.next = dummy_odd_head.next
    return dummy_even_head.next


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('even_odd_list_merge.py',
                                       'even_odd_list_merge.tsv',
                                       even_odd_merge_extensible))
