from typing import List

from binary_tree_node import BinaryTreeNode
from test_framework import generic_test


def inorder_traversal(tree: BinaryTreeNode) -> List[int]:
    """
    An elegant and fast iterative solution!
    But it is also difficult to come up with on your own in an interview setting.
    inorder_traversal_v1() version written below will be expected and sufficient.

    The time complexity is O(n), since the total time spent on each node is O(1). The space complexity is O(h), where h
    is the height of the tree. This space is allocated dynamically, specifically it is the maximum depth of the function
    call stack for the recursive implementation.
    """

    nodes, result = [], []

    while nodes or tree:
        if tree:
            nodes.append(tree)
            # Going left.
            tree = tree.left
        else:
            # Going up.
            tree = nodes.pop()
            result.append(tree.data)
            # Going right.
            tree = tree.right

    return result


def inorder_traversal_v1(tree: BinaryTreeNode) -> List[int]:
    """Iterative"""

    result = []

    nodes = [(tree, False)]
    while nodes:
        node, is_processed = nodes.pop()
        if node:
            if is_processed:
                result.append(node.data)
            else:
                nodes.append((node.right, False))
                nodes.append((node, True))
                nodes.append((node.left, False))

    return result


def inorder_traversal_recursive(tree: BinaryTreeNode) -> List[int]:
    """Recursive"""

    def in_traversal(tree: BinaryTreeNode, result: List[int]) -> None:
        if tree:
            in_traversal(tree.left, result)
            result.append(tree.data)
            in_traversal(tree.right, result)

    result = []
    if not tree:
        return result
    in_traversal(tree.left, result)
    result.append(tree.data)
    in_traversal(tree.right, result)
    return result


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('tree_inorder.py', 'tree_inorder.tsv',
                                       inorder_traversal))
