import functools

from binary_tree_node import BinaryTreeNode
from test_framework import generic_test
from test_framework.test_utils import enable_executor_hook


def reconstruct_preorder_using_iterator(
        preorder: list[int]) -> BinaryTreeNode | None:
    """
    #9.13

    Time complexity = O(n), n = len(preorder)
    Space complexity = O(n) on function call stack

    Test PASSED (3852/3852) [  <1 us]
    Average running time:   19 us
    Median running time:     2 us
    """

    def reconstruct_preorder_helper(preorder_iter) -> (BinaryTreeNode | None):
        subtree_key = next(preorder_iter)
        if subtree_key is None:
            return None
        left_subtree = reconstruct_preorder_helper(preorder_iter)
        right_subtree = reconstruct_preorder_helper(preorder_iter)
        return BinaryTreeNode(subtree_key, left_subtree, right_subtree)

    return reconstruct_preorder_helper(iter(preorder))


def reconstruct_preorder_using_nonlocal_index_variable(preorder: list[int]) -> (
        BinaryTreeNode | None):
    """
    Test PASSED (3852/3852) [  <1 us]
    Average running time:   25 us
    Median running time:     2 us

    Highly Preferred in Software Engineering Interviews. Fast to write,
    clean code structure, and demonstrates deep mastery of Pythonic scope.

    Acceptable in Enterprise Production Quality. Clean syntax, encapsulated
    inside the parent function, but harder to parallelize or decouple.
    """
    index = 0

    def reconstruct_preorder_helper() -> BinaryTreeNode | None:
        nonlocal index
        # Safety check to prevent IndexError if the list is malformed
        if index >= len(preorder):
            return None

        subtree_key = preorder[index]
        index += 1

        if subtree_key is None:
            return None

        left_subtree = reconstruct_preorder_helper()
        right_subtree = reconstruct_preorder_helper()
        return BinaryTreeNode(subtree_key, left_subtree, right_subtree)

    return reconstruct_preorder_helper()


def reconstruct_preorder_using_explicit_index_passing(
        preorder: list[int]) -> BinaryTreeNode | None:
    """
    Test PASSED (3852/3852) [  <1 us]
    Average running time:   30 us
    Median running time:     3 us

    Highly Preferred in Enterprise Production.
    Thread-safe, pure, and trivial to unit test in isolation.

    Neutral in Software Engineering Interviews. Clear logic, but slightly more
    verbose since you must return both the node and the new index.
    """
    def reconstruct_preorder_helper(index: int) -> tuple[BinaryTreeNode |
                                                         None, int]:
        # Safety check to prevent IndexError if the list is malformed
        if index >= len(preorder):
            return None, index

        subtree_key = preorder[index]

        # Base case: if we hit a null marker, move the index forward by 1
        if subtree_key is None:
            return None, index + 1

        # 1. Process left subtree starting right after the current node
        left_subtree, next_index = reconstruct_preorder_helper(index + 1)

        # 2. Process right subtree starting where the left subtree finished
        right_subtree, final_index = reconstruct_preorder_helper(next_index)

        # 3. Construct the current node and return the final index tracker
        root_node = BinaryTreeNode(subtree_key, left_subtree, right_subtree)
        return root_node, final_index

    # Start the recursion at index 0 and discard the final index from the return
    root, _ = reconstruct_preorder_helper(0)
    return root


@enable_executor_hook
def reconstruct_preorder_wrapper(executor, data):
    data = [None if x == 'null' else int(x) for x in data]
    return executor.run(functools.partial(
        reconstruct_preorder_using_iterator, data))


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('tree_from_preorder_with_null.py',
                                       'tree_from_preorder_with_null.tsv',
                                       reconstruct_preorder_wrapper))
