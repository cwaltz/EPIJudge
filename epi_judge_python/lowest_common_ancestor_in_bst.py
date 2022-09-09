import functools
from typing import Optional

from bst_node import BstNode
from test_framework import generic_test
from test_framework.binary_tree_utils import must_find_node
from test_framework.test_failure import TestFailure
from test_framework.test_utils import enable_executor_hook


# Input nodes are nonempty and s.data <= b.data.
def find_lca(tree: BstNode, s: BstNode, b: BstNode) -> Optional[BstNode]:
    """
    #14.4

    Time complexity = O(h), where h is the height of the tree.
    Space complexity = O(1)

    Test PASSED (951/951) [  <1 us]
    Average running time:   <1 us
    Median running time:    <1 us
    """
    # while not (s.data <= tree.data <= b.data):  # Current line also works in place of next line.
    while tree.data < s.data or b.data < tree.data:
        # Keep searching since tree is outside [s, b].
        while tree.data < s.data:
            tree = tree.right  # LCA must be in tree's right child.
        while b.data < tree.data:
            tree = tree.left  # LCA must be in tree's left child.
    # Now, s.data <= tree.data <= b.data.
    return tree


@enable_executor_hook
def lca_wrapper(executor, tree, s, b):
    result = executor.run(
        functools.partial(find_lca, tree, must_find_node(tree, s),
                          must_find_node(tree, b)))
    if result is None:
        raise TestFailure('Result can\'t be None')
    return result.data


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('lowest_common_ancestor_in_bst.py',
                                       'lowest_common_ancestor_in_bst.tsv',
                                       lca_wrapper))
