from list_node import ListNode


def print_linked_list_in_reverse(head: ListNode) -> None:
    """
    #8.0

    Time complexity = O(n), where n is the number of nodes in the list.
    Space complexity = O(n)
    """
    nodes = []
    while head:
        nodes.append(head.data)
        head = head.next
    while nodes:
        print(nodes.pop())
