from typing import List

from binary_tree_node import BinaryTreeNode
from test_framework import generic_test


def binary_tree_depth_order(tree: BinaryTreeNode) -> List[List[int]]:
    """
    Since each node is enqueued and dequeued exactly once, the time complexity is O(n).
    The space complexity is O(m), where m is the maximum number of nodes at any single depth.
    """
    result: List[List[int]] = []
    if not tree:
        return result

    level = [tree]
    while level:
        result.append([node.data for node in level])
        level = [
            child
            for node in level
            for child in (node.left, node.right)
            if child
        ]
    return result


def binary_tree_depth_order_v1(tree: BinaryTreeNode) -> List[List[int]]:
    result: List[List[int]] = []
    if not tree:
        return result

    level = [tree]
    while level:
        result.append([node.data for node in level])
        next_level = []
        for node in level:
            if node.left:
                next_level.append(node.left)
            if node.right:
                next_level.append(node.right)
        level = next_level
    return result


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('tree_level_order.py',
                                       'tree_level_order.tsv',
                                       binary_tree_depth_order))
