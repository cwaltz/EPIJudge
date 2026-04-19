import collections
from typing import List

from binary_tree_node import BinaryTreeNode
from test_framework import generic_test


def binary_tree_depth_order(tree: BinaryTreeNode) -> List[List[int]]:
    """
    #8.6

    Time complexity = O(n), since each node is enqueued & dequeued exactly once.
    Space complexity = O(m), where m = max number of nodes at any single depth.

    Test PASSED (3852/3852) [  <1 us]
    Average running time:    6 us
    Median running time:     1 us
    """
    if not tree:
        return []

    result = []
    level = [tree]
    while level:
        values, next_level = [], []
        for node in level:
            values.append(node.data)
            if node.left:
                next_level.append(node.left)
            if node.right:
                next_level.append(node.right)

        level = next_level
        result.append(values)

    return result


def binary_tree_depth_order_1(tree: BinaryTreeNode) -> List[List[int]]:
    """
    Test PASSED (3852/3852) [  <1 us]
    Average running time:    7 us
    Median running time:     1 us
    """
    if not tree:
        return []
    result = []
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


def binary_tree_depth_order_2(tree: BinaryTreeNode) -> List[List[int]]:
    """
    Test PASSED (3852/3852) [  <1 us]
    Average running time:   10 us
    Median running time:     2 us
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


def binary_tree_depth_order_3(tree: BinaryTreeNode) -> List[List[int]]:
    """
    Test PASSED (3852/3852) [  <1 us]
    Average running time:    9 us
    Median running time:     2 us
    """
    if not tree:
        return []
    curr_level = collections.deque([tree])
    result = []
    while curr_level:
        nodes = []
        next_level = collections.deque()
        while curr_level:
            node = curr_level.popleft()
            if node.left:
                next_level.append(node.left)
            if node.right:
                next_level.append(node.right)
            nodes.append(node.data)
        result.append(nodes)
        curr_level = next_level
    return result


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('tree_level_order.py',
                                       'tree_level_order.tsv',
                                       binary_tree_depth_order))
