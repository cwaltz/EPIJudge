from typing import List, Optional, Dict

from bst_node import BstNode
from test_framework import generic_test


def rebuild_bst_from_preorder(preorder_sequence: List[int]) -> Optional[
    BstNode]:
    """
    #14.5

    Time complexity = O(n log n) = O(n log n) + O(n) + O(n)
    Building the inorder sequence takes O(n log n) time due to sorting, building
    the hash table takes O(n) time and the recursive reconstruction spends O(1)
    time per node.
    Space complexity = O(n) = O(n) + O(n) + O(h)
    = size of the inorder sequence O(n) + size of the hash table O(n) + maximum
    depth of function call stack O(h)

    Test PASSED (950/950) [  <1 us]
    Average running time:  300 us
    Median running time:    41 us
    """

    def rebuild_tree_from_preorder_inorder_traversals(pre_start, pre_end,
                                                      in_start, in_end):
        if pre_end <= pre_start or in_end <= in_start:
            return None
        root_inorder_idx = inorder_idx[preorder_sequence[pre_start]]
        left_subtree_size = root_inorder_idx - in_start
        return BstNode(
            preorder_sequence[pre_start],
            rebuild_tree_from_preorder_inorder_traversals(
                pre_start + 1, pre_start + 1 + left_subtree_size, in_start,
                root_inorder_idx),
            rebuild_tree_from_preorder_inorder_traversals(
                pre_start + 1 + left_subtree_size, pre_end,
                root_inorder_idx + 1, in_end)
        )

    if len(preorder_sequence) == 0:
        return None
    inorder_sequence: List[int] = sorted(preorder_sequence)
    inorder_idx: Dict[int, int] = {value: index for index, value in
                                   enumerate(inorder_sequence)}
    return rebuild_tree_from_preorder_inorder_traversals(pre_start=0,
                                                         pre_end=len(
                                                             preorder_sequence),
                                                         in_start=0,
                                                         in_end=len(
                                                             inorder_sequence))


def rebuild_bst_from_preorder_linear_time(preorder_sequence: List[int]) -> \
        Optional[BstNode]:
    """
    Time complexity = O(n), since it performs a constant amount of work per node

    Test PASSED (950/950) [   1 us]
    Average running time:  286 us
    Median running time:    39 us
    """

    # TODO: Yet to be understood!
    def rebuild_bst_from_preorder_on_value_range(lower_bound, upper_bound):
        if root_idx[0] == len(preorder_sequence):
            return None

        root = preorder_sequence[root_idx[0]]
        if not lower_bound <= root <= upper_bound:
            return None
        root_idx[0] += 1
        # Note that rebuild_bst_from_preorder_on_value_range updates root_idx[0]
        # So the order of following two calls are critical.
        left_subtree = rebuild_bst_from_preorder_on_value_range(lower_bound,
                                                                root)
        right_subtree = rebuild_bst_from_preorder_on_value_range(root,
                                                                 upper_bound)
        return BstNode(root, left_subtree, right_subtree)

    root_idx = [0]  # Tracks current subtree.
    return rebuild_bst_from_preorder_on_value_range(float('-inf'), float('inf'))


def rebuild_bst_from_preorder_slow(preorder_sequence: List[int]
                                   ) -> Optional[BstNode]:
    """
    Time complexity = O(n log n) for a balanced BST
                    = O(n ** 2) in the worst case (a left-skewed tree)
    Space complexity = O(n)

    The worst-case input for this algorithm is the pre-order sequence
    corresponding to a left-skewed tree. The worst-case time complexity
    satisfies the recurrence W(n) = W(n - 1) + O(n), which solves to O(n ** 2).
    The best-case input is a sequence corresponding to a right-skewed tree, and
    the corresponding time complexity is O(n). When the sequence corresponds to
    a balanced BST, the time complexity is given by B(n) = 2B(n/2) + O(n),
    which solves to O(n log n).

    Test PASSED (950/950) [  <1 us]
    Average running time:  483 us
    Median running time:    64 us
    """

    if not preorder_sequence:
        return None

    transition_point = next(
        (i
         for i, a in enumerate(preorder_sequence) if a > preorder_sequence[0]),
        len(preorder_sequence))
    return BstNode(
        preorder_sequence[0],
        rebuild_bst_from_preorder_slow(preorder_sequence[1:transition_point]),
        rebuild_bst_from_preorder_slow(preorder_sequence[transition_point:]))


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('bst_from_preorder.py',
                                       'bst_from_preorder.tsv',
                                       rebuild_bst_from_preorder))
