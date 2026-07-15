import functools

from binary_tree_with_parent_prototype import BinaryTreeNode
from test_framework import generic_test
from test_framework.binary_tree_utils import must_find_node
from test_framework.test_failure import TestFailure
from test_framework.test_utils import enable_executor_hook


def lca_production(node0: BinaryTreeNode | None,
                   node1: BinaryTreeNode | None) -> BinaryTreeNode | None:
    """
    #12.4

    Time Complexity: O(d0 + d1)
    Space Complexity: O(d0 + d1)
        where d0 is the distance from the LCA to the first node,
          and d1 is the distance from the LCA to the second node

    Test PASSED (948/948) [   2 us]
    Average running time:    2 us
    Median running time:     2 us
    """
    # 1. Guard against null inputs
    if not node0 or not node1:
        return None

    iter0, iter1 = node0, node1
    # 2. Store object IDs to prevent bugs if __hash__ is overridden based on
    # node value
    visited_ids: set[int] = set()

    while iter0 or iter1:
        if iter0:
            if id(iter0) in visited_ids:
                return iter0
            visited_ids.add(id(iter0))
            iter0 = iter0.parent

        if iter1:
            if id(iter1) in visited_ids:
                return iter1
            visited_ids.add(id(iter1))
            iter1 = iter1.parent

    raise ValueError('node0 and node1 are not in the same tree')


def lca_interview(node0: BinaryTreeNode,
                  node1: BinaryTreeNode) -> BinaryTreeNode | None:
    """
    Time Complexity: O(d0 + d1)
    Space Complexity: O(d0 + d1)
        where d0 is the distance from the LCA to the first node,
          and d1 is the distance from the LCA to the second node

    Test PASSED (948/948) [   1 us]
    Average running time:    1 us
    Median running time:     1 us
    """

    iter0, iter1 = node0, node1
    nodes_on_path_to_root: set[BinaryTreeNode] = set()
    while iter0 or iter1:
        # Ascend tree in tandem for these two nodes.
        if iter0:
            if iter0 in nodes_on_path_to_root:
                return iter0
            nodes_on_path_to_root.add(iter0)
            iter0 = iter0.parent
        if iter1:
            if iter1 in nodes_on_path_to_root:
                return iter1
            nodes_on_path_to_root.add(iter1)
            iter1 = iter1.parent
    raise ValueError('node0 and node1 are not in the same tree')


@enable_executor_hook
def lca_wrapper(executor, tree, node0, node1):
    result = executor.run(
        functools.partial(lca_interview, must_find_node(tree, node0),
                          must_find_node(tree, node1)))

    if result is None:
        raise TestFailure('Result can\'t be None')
    return result.data


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main(
            'lowest_common_ancestor_close_ancestor.py',
            'lowest_common_ancestor.tsv', lca_wrapper))
