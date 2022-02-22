from typing import List

from binary_tree_node import BinaryTreeNode
from test_framework import generic_test


def preorder_traversal(tree: BinaryTreeNode) -> List[int]:
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
                nodes.append((node.left, False))
                nodes.append((node, True))

    return result


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('tree_preorder.py', 'tree_preorder.tsv',
                                       preorder_traversal))
