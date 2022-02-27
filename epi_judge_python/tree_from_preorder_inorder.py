from typing import List, Optional

from binary_tree_node import BinaryTreeNode
from test_framework import generic_test


def binary_tree_from_preorder_inorder(preorder: List[int],
                                      inorder: List[int]) -> BinaryTreeNode:
    """
    The time complexity is O(n)-building the hash table takes O(n) time and the recursive reconstruction spends O(1)
    time per node. The space complexity is O(n + h) = O(n)-the size of the hash table plus the maximum depth of the
    function call stack.
    """

    key_to_inorder_idx = {key: index for index, key in enumerate(inorder)}

    # Builds the subtree with preorder[pre_start:pre_end] and
    # inorder[in_start:in_end].
    def subtree_from_preorder_inorder(pre_start: int, pre_end: int,
                                      in_start: int, in_end: int) -> Optional[BinaryTreeNode]:
        if pre_start < pre_end and in_start < in_end:
            root_in_idx = key_to_inorder_idx[preorder[pre_start]]
            left_subtree_size = root_in_idx - in_start
            return BinaryTreeNode(
                preorder[pre_start],
                # Recursively builds the left subtree.
                subtree_from_preorder_inorder(
                    pre_start + 1, pre_start + 1 + left_subtree_size,
                    in_start, root_in_idx),
                # Recursively builds the right subtree.
                subtree_from_preorder_inorder(
                    pre_start + 1 + left_subtree_size, pre_end,
                    root_in_idx + 1, in_end)
            )
        return None

    return subtree_from_preorder_inorder(pre_start=0,
                                         pre_end=len(preorder),
                                         in_start=0,
                                         in_end=len(inorder))


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('tree_from_preorder_inorder.py',
                                       'tree_from_preorder_inorder.tsv',
                                       binary_tree_from_preorder_inorder))
