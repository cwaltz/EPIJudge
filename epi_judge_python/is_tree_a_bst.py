import collections

from binary_tree_node import BinaryTreeNode
from test_framework import generic_test


def is_binary_tree_bst(tree: BinaryTreeNode) -> bool:
    """
    #14.1

    Time complexity = O(n), where n is the number of nodes
    Space complexity = O(h), where h is the height of the tree

    DFS approach

    Test PASSED (3139/3139) [  <1 us]
    Average running time:    1 us
    Median running time:     1 us
    """
    def are_keys_in_range(tree,
                          low_range=float('-inf'),
                          high_range=float('inf')):
        if not tree:
            return True
        elif not low_range <= tree.data <= high_range:
            return False
        return (are_keys_in_range(tree.left, low_range, tree.data)
                and are_keys_in_range(tree.right, tree.data, high_range))

    return are_keys_in_range(tree)


def is_binary_tree_bst_iterative(tree: BinaryTreeNode) -> bool:
    """
    Time complexity = O(n), where n is the number of nodes
    Space complexity = O(n)

    BFS approach

    Test PASSED (3139/3139) [  <1 us]
    Average running time:   48 us
    Median running time:    42 us
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


def is_binary_tree_bst_iterative_without_namedtuple(tree: BinaryTreeNode) -> bool:
    """
    Time complexity = O(n), where n is the number of nodes
    Space complexity = O(n)

    BFS approach

    Test PASSED (3139/3139) [  <1 us]
    Average running time:    2 us
    Median running time:     2 us
    """
    if not tree:
        return True
    # QueueEntry = collections.namedtuple('QueueEntry', ('node', 'lower', 'upper'))
    bfs_queue = collections.deque([(tree, float('-inf'), float('inf'))])

    while bfs_queue:
        front = bfs_queue.popleft()
        if not front[1] <= front[0].data <= front[2]:
            return False
        if front[0].left:
            bfs_queue.append((front[0].left, front[1], front[0].data))
        if front[0].right:
            bfs_queue.append((front[0].right, front[0].data, front[2]))
    return True


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('is_tree_a_bst.py', 'is_tree_a_bst.tsv',
                                       is_binary_tree_bst))
