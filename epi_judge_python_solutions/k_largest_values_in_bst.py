from typing import List

from bst_node import BstNode
from test_framework import generic_test, test_utils


def find_k_largest_in_bst(tree: BstNode, k: int) -> List[int]:
    """
    Time complexity  = O(h + k)
    Space complexity = O(h + k)

    The complexity bound comes from the observation that the number of times the program descends in the tree can be at
    most h more than the number of times it ascends the tree, and each ascent happens after we visit a node in the
    result. After k nodes have been added to the result, the program stops.

    Test PASSED (949/949) [   4 us]
    Average running time:   46 us
    Median running time:     7 us
    """
    def find_k_largest_in_bst_helper(tree):
        # Perform reverse inorder traversal.
        if tree and len(k_largest_elements) < k:
            find_k_largest_in_bst_helper(tree.right)
            if len(k_largest_elements) < k:
                k_largest_elements.append(tree.data)
                find_k_largest_in_bst_helper(tree.left)

    k_largest_elements: List[int] = []
    find_k_largest_in_bst_helper(tree)
    return k_largest_elements


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('k_largest_values_in_bst.py',
                                       'k_largest_values_in_bst.tsv',
                                       find_k_largest_in_bst,
                                       test_utils.unordered_compare))
