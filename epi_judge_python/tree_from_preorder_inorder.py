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


def binary_tree_from_preorder_inorder_shortest(
        preorder: List[int], inorder: List[int]) -> Optional[BinaryTreeNode]:
    """
    Source: Neetcode :)
    https://github.com/neetcode-gh/leetcode/blob/main/python/105-Construct-Binary-Tree-from-Preorder-and-Inorder-Traversal.py
    # TODO: Watch Neetcode's video & calculate time & space complexities.

    Test PASSED (3852/3852) [  <1 us]
    Average running time:   65 us
    Median running time:     6 us
    """
    if not preorder or not inorder:
        return None

    root = BinaryTreeNode(preorder[0])
    mid = inorder.index(preorder[0])
    root.left = binary_tree_from_preorder_inorder(
        preorder[1: mid + 1], inorder[:mid])
    root.right = binary_tree_from_preorder_inorder(
        preorder[mid + 1:], inorder[mid + 1:])
    return root


def binary_tree_from_preorder_inorder_short(
        preorder: List[int], inorder: List[int]) -> BinaryTreeNode:
    """
    Source:
    https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/solutions/34543/simple-o-n-without-map/
    # TODO: To be understood yet!

    Test PASSED (3852/3852) [  <1 us]
    Average running time:   49 us
    Median running time:     5 us
    """
    def build(stop):
        if inorder and inorder[-1] != stop:
            root = BinaryTreeNode(preorder.pop())
            root.left = build(root.data)
            inorder.pop()
            root.right = build(stop)
            return root

    preorder.reverse()
    inorder.reverse()
    return build(None)


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('tree_from_preorder_inorder.py',
                                       'tree_from_preorder_inorder.tsv',
                                       binary_tree_from_preorder_inorder))
