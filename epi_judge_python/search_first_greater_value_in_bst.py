from bst_node import BstNode
from test_framework import generic_test


def find_first_greater_than_k(tree: BstNode, key: int) -> None | BstNode:
    """
    #14.2

    Time complexity = O(h), where h is the height of the tree.
    Space complexity = O(1)

    Test PASSED (949/949) [  <1 us]
    Average running time:   <1 us
    Median running time:    <1 us
    """
    subtree, first_so_far = tree, None
    while subtree:
        if key < subtree.data:
            first_so_far, subtree = subtree, subtree.left
        else:  # Root and all keys in left subtree are <= key, so skip them.
            subtree = subtree.right
    return first_so_far


def find_first_greater_than_k_wrapper(tree: BstNode, key: int):
    result = find_first_greater_than_k(tree, key)
    return result.data if result else -1


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main(
            'search_first_greater_value_in_bst.py',
            'search_first_greater_value_in_bst.tsv',
            find_first_greater_than_k_wrapper))
