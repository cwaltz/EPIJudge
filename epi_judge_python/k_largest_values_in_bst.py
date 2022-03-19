from typing import List

from bst_node import BstNode
from test_framework import generic_test, test_utils


def find_k_largest_in_bst(tree: BstNode, k: int) -> List[int]:
    """
    Test PASSED (949/949) [   4 us]
    Average running time:   41 us
    Median running time:     7 us
    """
    def right_to_left_traversal(tree):
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
