import functools
from typing import Optional

from binary_tree_node import BinaryTreeNode
from test_framework import generic_test
from test_framework.binary_tree_utils import must_find_node, strip_parent_link
from test_framework.test_failure import TestFailure
from test_framework.test_utils import enable_executor_hook


def lca(tree: BinaryTreeNode, node0: BinaryTreeNode,
        node1: BinaryTreeNode) -> Optional[BinaryTreeNode]:
    """
    #9.3

    Time complexity = O(n), where n is the number of nodes in the tree.
    Space complexity = O(h) = O(n) in the worst case.

    DFS, recursive.

    Test PASSED (948/948) [   2 us]
    Average running time:   83 us
    Median running time:    10 us
    """
    if tree in [None, node0, node1]:
        return tree
    left_node = lca(tree.left, node0, node1)
    right_node = lca(tree.right, node0, node1)
    if left_node and right_node:
        return tree
    return left_node or right_node


@enable_executor_hook
def lca_wrapper(executor, tree, key1, key2):
    strip_parent_link(tree)
    result = executor.run(
        functools.partial(lca, tree, must_find_node(tree, key1),
                          must_find_node(tree, key2)))

    if result is None:
        raise TestFailure('Result can\'t be None')
    return result.data


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('lowest_common_ancestor.py',
                                       'lowest_common_ancestor.tsv',
                                       lca_wrapper))
