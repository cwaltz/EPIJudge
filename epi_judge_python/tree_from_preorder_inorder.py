from typing import List, Optional

from binary_tree_node import BinaryTreeNode
from test_framework import generic_test


def binary_tree_from_preorder_inorder(preorder: List[int],
                                      inorder: List[int]) -> BinaryTreeNode:
    """
    #9.11

    Time complexity = O(n)
    Building the hash table takes O(n) time and the recursive reconstruction
    spends O(1) time per node.
    Space complexity = O(n) = the size of the hash table O(n) + the maximum
    depth of the function call stack O(h)

    Test PASSED (3852/3852) [   1 us]
    Average running time:   53 us
    Median running time:     6 us
    """
    node_to_inorder_idx = {data: i for i, data in enumerate(inorder)}

    # Builds the subtree with preorder[preorder_start:preorder_end] and
    # inorder[inorder_start:inorder_end].
    def binary_tree_from_preorder_inorder_helper(
            preorder_start: int, preorder_end: int, inorder_start: int,
            inorder_end: int) -> Optional[BinaryTreeNode]:
        if preorder_end <= preorder_start or inorder_end <= inorder_start:
            return None

        root_inorder_idx = node_to_inorder_idx[preorder[preorder_start]]
        left_subtree_size = root_inorder_idx - inorder_start
        return BinaryTreeNode(
            preorder[preorder_start],
            # Recursively builds the left subtree.
            binary_tree_from_preorder_inorder_helper(
                preorder_start + 1, preorder_start + 1 + left_subtree_size,
                inorder_start, root_inorder_idx),
            # Recursively builds the right subtree.
            binary_tree_from_preorder_inorder_helper(
                preorder_start + 1 + left_subtree_size, preorder_end,
                root_inorder_idx + 1, inorder_end))

    return binary_tree_from_preorder_inorder_helper(preorder_start=0,
                                                    preorder_end=len(preorder),
                                                    inorder_start=0,
                                                    inorder_end=len(inorder))


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('tree_from_preorder_inorder.py',
                                       'tree_from_preorder_inorder.tsv',
                                       binary_tree_from_preorder_inorder))
