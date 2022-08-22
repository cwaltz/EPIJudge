import functools

from list_node import ListNode
from test_framework import generic_test
from test_framework.test_utils import enable_executor_hook


# Insert new_node after node.
def insert_after(node: ListNode, new_node: ListNode) -> None:
    """
    #7.0

    Time complexity = O(1)
    Space complexity = O(1)

    Test PASSED (504/504) [  <1 us]
    Average running time:   <1 us
    Median running time:    <1 us
    """
    new_node.next = node.next
    node.next = new_node


@enable_executor_hook
def insert_list_wrapper(executor, l, node_idx, new_node_data):
    node = l
    for _ in range(node_idx - 1):
        node = node.next
    new_node = ListNode(new_node_data)

    executor.run(functools.partial(insert_after, node, new_node))

    return l


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('insert_in_list.py',
                                       'insert_in_list.tsv',
                                       insert_list_wrapper))
