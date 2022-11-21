from typing import List

from bst_node import BstNode
from test_framework import generic_test, test_utils


def find_k_largest_in_bst(tree: BstNode, k: int) -> List[int]:
    """
    #14.3

    Time complexity = O(h + k)
    Space complexity = O(h + k)

    The complexity bound comes from the observation that the number of times the
    program descends in the tree can be at most h more than the number of times
    it ascends the tree, and each ascent happens after we visit a node in the
    result. After k nodes have been added to the result, the program stops.

    Test PASSED (949/949) [   2 us]
    Average running time:   28 us
    Median running time:     4 us
    """
    k_largest, stack = [], []
    while True:
        while tree:
            stack.append(tree)
            tree = tree.right
        tree = stack.pop()
        k_largest.append(tree.data)
        k -= 1
        if k == 0:
            return k_largest
        tree = tree.left


def find_k_largest_in_bst_recursive(tree: BstNode, k: int) -> List[int]:
    """
    #14.3

    Time complexity = O(h + k)
    Space complexity = O(h + k)

    The complexity bound comes from the observation that the number of times the
    program descends in the tree can be at most h more than the number of times
    it ascends the tree, and each ascent happens after we visit a node in the
    result. After k nodes have been added to the result, the program stops.

    Test PASSED (949/949) [   3 us]
    Average running time:   35 us
    Median running time:     5 us
    """
    def right_to_left_traversal(tree):
        # Perform reverse inorder traversal.
        if tree:
            right_to_left_traversal(tree.right)
            if len(k_largest) < k:
                k_largest.append(tree.data)
            else:
                return
            right_to_left_traversal(tree.left)

    k_largest = []
    right_to_left_traversal(tree)
    return k_largest


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('k_largest_values_in_bst.py',
                                       'k_largest_values_in_bst.tsv',
                                       find_k_largest_in_bst,
                                       test_utils.unordered_compare))
