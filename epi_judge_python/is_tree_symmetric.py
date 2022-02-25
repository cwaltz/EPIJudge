from binary_tree_node import BinaryTreeNode
from test_framework import generic_test


def is_symmetric(tree: BinaryTreeNode) -> bool:
    """
    The time complexity and space complexity are O(n) and O(h), respectively,
    where n is the number of nodes in the tree and h is the height of the tree.
    """

    def are_subtrees_symmetric(subtree_0: BinaryTreeNode, subtree_1: BinaryTreeNode) -> bool:

        if not subtree_0 and not subtree_1:
            return True
        elif subtree_0 and subtree_1:
            return (subtree_0.data == subtree_1.data
                    and are_subtrees_symmetric(subtree_0.left, subtree_1.right)
                    and are_subtrees_symmetric(subtree_0.right, subtree_1.left))
        # One subtree is empty, and the other is not.
        return False

    return not tree or are_subtrees_symmetric(tree.left, tree.right)


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('is_tree_symmetric.py',
                                       'is_tree_symmetric.tsv', is_symmetric))
