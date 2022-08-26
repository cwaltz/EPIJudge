import collections

from typing import Tuple

from binary_tree_node import BinaryTreeNode
from test_framework import generic_test


def is_balanced_binary_tree(tree: BinaryTreeNode) -> bool:
    """
    #9.1

    Time complexity  = O(n), where n is the number of nodes of the tree.
    Space complexity = O(h), where h is the height of the tree.

    The program implements a postorder traversal with some calls possibly being eliminated because of early termination.
    Specifically, if any left subtree is not height-balanced we do not need to visit the corresponding right subtree.
    The function call stack corresponds to a sequence of calls from the root through the unique path to the current
    node, and the stack height is therefore bounded by the height of the tree, leading to an O(h) space bound.
    The time complexity is the same as that for a postorder traversal, namely O(n).

    Test PASSED (3852/3852) [  38 us]
    Average running time:   66 us
    Median running time:    43 us
    """
    BalancedStatusWithHeight = collections.namedtuple(
        'BalancedStatusWithHeight', ('balanced', 'height'))

    # First value of the return value indicates if tree is balanced,
    # and if balanced the second value of the return value is the height of tree.
    def check_balanced(node: BinaryTreeNode) -> BalancedStatusWithHeight:
        if not node:
            return BalancedStatusWithHeight(balanced=True, height=-1)

        left_result = check_balanced(node.left)
        if not left_result.balanced:
            return left_result

        right_result = check_balanced(node.right)
        if not right_result.balanced:
            return right_result

        is_balanced = abs(left_result.height - right_result.height) <= 1
        height = max(left_result.height, right_result.height) + 1
        return BalancedStatusWithHeight(is_balanced, height)

    return check_balanced(tree).balanced


def is_balanced_binary_tree_faster(tree: BinaryTreeNode) -> bool:
    """
    Faster solution without a namedtuple!

    Test PASSED (3852/3852) [   1 us]
    Average running time:   11 us
    Median running time:     5 us
    """
    # First value of the return value indicates if tree is balanced,
    # and if balanced the second value of the return value is the height of tree.
    def is_subtree_height_balanced(node: BinaryTreeNode) -> Tuple[bool, int]:
        if not node:
            return True, -1

        left_result = is_subtree_height_balanced(node.left)
        if not left_result[0]:
            return left_result

        right_result = is_subtree_height_balanced(node.right)
        if not right_result[0]:
            return right_result

        is_balanced = abs(left_result[1] - right_result[1]) <= 1
        height = max(left_result[1], right_result[1]) + 1
        return is_balanced, height

    return is_subtree_height_balanced(tree)[0]


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('is_tree_balanced.py',
                                       'is_tree_balanced.tsv',
                                       is_balanced_binary_tree))
