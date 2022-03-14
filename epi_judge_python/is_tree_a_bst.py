import collections

from binary_tree_node import BinaryTreeNode
from test_framework import generic_test


def is_binary_tree_bst(tree: BinaryTreeNode) -> bool:
    """
    Time complexity  = O(n), where n is the number of nodes
    Space complexity = O(h), where h is the height of the tree

    DFS approach

    Test PASSED (3139/3139) [   2 us]
    Average running time:    2 us
    Median running time:     2 us
    """

    def is_binary_tree_bst_helper(tree, low, high):
        if not tree:
            return True
        if not low <= tree.data <= high:
            return False
        return (
            is_binary_tree_bst_helper(tree.left, low, tree.data) and
            is_binary_tree_bst_helper(tree.right, tree.data, high)
        )

    return is_binary_tree_bst_helper(tree, float('-inf'), float('inf'))


def is_binary_tree_bst_v1(tree: BinaryTreeNode) -> bool:
    """
    Time complexity  = O(n), where n is the number of nodes
    Space complexity = O(n)

    BFS approach

    Test PASSED (3139/3139) [  <1 us]
    Average running time:   72 us
    Median running time:    62 us
    """

    if not tree:
        return True
    QueueEntry = collections.namedtuple('QueueEntry', ('node', 'lower', 'upper'))
    bfs_queue = collections.deque([QueueEntry(tree, float('-inf'), float('inf'))])

    while bfs_queue:
        front = bfs_queue.popleft()
        if not front.lower <= front.node.data <= front.upper:
            return False
        if front.node.left:
            bfs_queue.append(QueueEntry(front.node.left, front.lower, front.node.data))
        if front.node.right:
            bfs_queue.append(QueueEntry(front.node.right, front.node.data, front.upper))
    return True


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('is_tree_a_bst.py', 'is_tree_a_bst.tsv',
                                       is_binary_tree_bst))
