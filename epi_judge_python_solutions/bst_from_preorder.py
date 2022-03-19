from typing import List, Optional

from bst_node import BstNode
from test_framework import generic_test


def rebuild_bst_from_preorder(preorder_sequence: List[int]) -> Optional[BstNode]:
    """
    The worst-case time complexity is O(n), since it performs a constant amount of work per node.
    """

    def rebuild_bst_from_preorder_on_value_range(lower_bound, upper_bound):
        if root_idx[0] == len(preorder_sequence):
            return None

        root = preorder_sequence[root_idx[0]]
        if not lower_bound <= root <= upper_bound:
            return None
        root_idx[0] += 1
        # Note that rebuild_bst_from_preorder_on_value_range updates root_idx[0].
        # So the order of following two calls are critical.
        left_subtree = rebuild_bst_from_preorder_on_value_range(lower_bound, root)
        right_subtree = rebuild_bst_from_preorder_on_value_range(root, upper_bound)
        return BstNode(root, left_subtree, right_subtree)

    root_idx = [0]  # Tracks current subtree.
    return rebuild_bst_from_preorder_on_value_range(float('-inf'), float('inf'))


def rebuild_bst_from_preorder_v0(preorder_sequence: List[int]
                                 ) -> Optional[BstNode]:
    """
    The worst-case input for this algorithm is the pre-order sequence corresponding to a left-skewed tree.
    The worst-case time complexity satisfies the recurrence W(n) = W(n - 1) + O(n), which solves to O(n ** 2).
    The best-case input is a sequence corresponding to a right-skewed tree, and the corresponding time complexity is
    O(n). When the sequence corresponds to a balanced BST, the time complexity is given by B(n) = 2B(n/2) + O(n),
    which solves to O(n log n).
    """

    if not preorder_sequence:
        return None

    transition_point = next(
        (i
         for i, a in enumerate(preorder_sequence) if a > preorder_sequence[0]),
        len(preorder_sequence))
    return BstNode(
        preorder_sequence[0],
        rebuild_bst_from_preorder(preorder_sequence[1:transition_point]),
        rebuild_bst_from_preorder(preorder_sequence[transition_point:]))


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('bst_from_preorder.py',
                                       'bst_from_preorder.tsv',
                                       rebuild_bst_from_preorder))
