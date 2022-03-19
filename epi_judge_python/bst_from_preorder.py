from typing import List, Optional, Dict

from bst_node import BstNode
from test_framework import generic_test


def rebuild_bst_from_preorder(preorder_sequence: List[int]
                              ) -> Optional[BstNode]:
    """
    Time complexity = O(n log n) = O(n log n) for sorting + O(n) for BST construction (O(1) time spent per node)
    Space complexity = O(h) = height of the tree (space taken on function call stack)

    Test PASSED (950/950) [   3 us]
    Average running time:  352 us
    Median running time:    47 us
    """

    def rebuild_bst_helper(pre_start: int, pre_end: int, in_start: int, in_end: int) -> Optional[BstNode]:
        if pre_start < pre_end and in_start < in_end:
            root_in_idx = inorder_idx[preorder_sequence[pre_start]]
            left_subtree_size = root_in_idx - in_start
            # right_subtree_size = in_end - root_in_idx
            return BstNode(
                preorder_sequence[pre_start],
                rebuild_bst_helper(pre_start + 1, pre_start + 1 + left_subtree_size, in_start, root_in_idx),
                rebuild_bst_helper(pre_start + 1 + left_subtree_size, pre_end, root_in_idx + 1, in_end)
            )
        else:
            return None

    inorder_sequence: List[int] = sorted(preorder_sequence)
    inorder_idx: Dict[int, int] = {v: i for i, v in enumerate(inorder_sequence)}
    return rebuild_bst_helper(0, len(preorder_sequence), 0, len(inorder_sequence))


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('bst_from_preorder.py',
                                       'bst_from_preorder.tsv',
                                       rebuild_bst_from_preorder))
