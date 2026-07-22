import bisect

from bst_node import BstNode
from test_framework import generic_test


# Linear time solutions


def rebuild_bst_from_preorder(preorder_sequence: list[int]) -> BstNode | None:
    """
    #14.5

    Iteratively reconstructs a BST from a preorder sequence in linear time

    Best solution for both - enterprise production environment and software
        engineering interview

    Time complexity = O(n), where n = len(preorder_sequence)
    Space complexity = O(h), where h = height of the tree

    Test PASSED (950/950) [  <1 us]
    Average running time:  129 us
    Median running time:    18 us
    """
    if not preorder_sequence:
        return None

    # The first element is always the root of the BST
    root = BstNode(preorder_sequence[0])
    stack = [root]

    # Iterate through the remaining elements
    for i in range(1, len(preorder_sequence)):
        val = preorder_sequence[i]
        node = BstNode(val)

        # If the value is smaller than the top of the stack,
        # it is the left child of the last inserted node.
        if val < stack[-1].data:
            stack[-1].left = node
        else:
            # If the value is greater, we are moving to a right subtree.
            # We must backtrack by popping from the stack until we find
            # the correct parent node. The parent is the last popped node
            # whose value is less than the current value.
            parent = stack[-1]
            while stack and stack[-1].data < val:
                parent = stack.pop()

            parent.right = node

        # The newly inserted node always goes onto the stack,
        # as it might have children of its own.
        stack.append(node)

    return root


def rebuild_bst_from_preorder_using_nonlocal(
        preorder_sequence: list[int]) -> BstNode | None:
    """
    Recursive linear time idiomatic solution using nonlocal keyword

    Time complexity = O(n)
    Space complexity = O(h) for the recursion stack

    Test PASSED (950/950) [  <1 us]
    Average running time:  143 us
    Median running time:    22 us
    """
    if not preorder_sequence:
        return None

    root_idx = 0  # Use a standard integer instead of a list hack
    length = len(preorder_sequence)

    def build_subtree(lower_bound: float | int, upper_bound: float | int) -> (
            BstNode | None):
        nonlocal root_idx  # Allows modification of the outer scope integer

        if root_idx == length:
            return None

        root_val = preorder_sequence[root_idx]

        if not (lower_bound <= root_val <= upper_bound):
            return None

        # Node belongs in this subtree, consume it
        root_idx += 1

        return BstNode(
            root_val,
            build_subtree(lower_bound, root_val),
            build_subtree(root_val, upper_bound)
        )

    # Build the tree
    root = build_subtree(float('-inf'), float('inf'))

    # Production safety: Ensure the entire sequence was valid
    if root_idx != length:
        raise ValueError(
            "Input sequence is not a valid preorder traversal of a BST.")

    return root


def rebuild_bst_from_preorder_with_boxed_index(
        preorder_sequence: list[int]) -> BstNode | None:
    """
    Recursive linear time non-idiomatic solution using boxing

    Time complexity = O(n), since it performs a constant amount of work per node
    Space complexity = O(h) = O(log n) on function call stack

    Test PASSED (950/950) [  <1 us]
    Average running time:  171 us
    Median running time:    27 us
    """

    def rebuild_bst_from_preorder_on_value_range(
            lower_bound: float | int, upper_bound: float | int) -> (
            BstNode | None):

        if root_idx[0] == len(preorder_sequence):
            return None

        root_data = preorder_sequence[root_idx[0]]
        if not lower_bound <= root_data <= upper_bound:
            return None

        root_idx[0] += 1
        # Note that rebuild_bst_from_preorder_on_value_range updates root_idx[0]
        # So the order of following two calls are critical.
        left_subtree = rebuild_bst_from_preorder_on_value_range(lower_bound,
                                                                root_data)
        right_subtree = rebuild_bst_from_preorder_on_value_range(root_data,
                                                                 upper_bound)
        return BstNode(root_data, left_subtree, right_subtree)

    root_idx = [0]  # Tracks current subtree.
    return rebuild_bst_from_preorder_on_value_range(float('-inf'), float('inf'))


# Solutions that take longer than linear time


def rebuild_bst_from_preorder_using_bisect(
        preorder_sequence: list[int]) -> BstNode | None:
    """
    Time complexity = O(n log n) in the worst case

    Test PASSED (950/950) [  <1 us]
    Average running time:  135 us
    Median running time:    20 us
    """

    def rebuild_bst_from_preorder_helper(
            first: int, last: int) -> BstNode | None:
        if first >= last:
            return None

        root_val = preorder_sequence[first]
        idx = bisect.bisect_left(preorder_sequence, root_val, first + 1, last)
        return BstNode(root_val,
                       rebuild_bst_from_preorder_helper(first + 1, idx),
                       rebuild_bst_from_preorder_helper(idx, last))

    if not preorder_sequence:
        return None

    return rebuild_bst_from_preorder_helper(0, len(preorder_sequence))


def rebuild_bst_from_preorder_using_sorting(preorder_sequence: list[int]) -> (
        BstNode | None):
    """
    Time complexity = O(n log n) = O(n log n) + O(n) + O(n)
    Building the inorder sequence takes O(n log n) time due to sorting, building
    the hash table takes O(n) time and the recursive reconstruction spends O(1)
    time per node.
    Space complexity = O(n) = O(n) + O(n) + O(h)
    = size of the inorder sequence O(n) + size of the hash table O(n) + maximum
    depth of function call stack O(h)

    Test PASSED (950/950) [  <1 us]
    Average running time:  180 us
    Median running time:    27 us
    """

    def rebuild_tree_from_preorder_inorder_traversals(
            pre_start: int, pre_end: int, in_start: int, in_end: int) -> (
            BstNode | None):
        if pre_end <= pre_start or in_end <= in_start:
            return None
        root_inorder_idx = inorder_idx[preorder_sequence[pre_start]]
        left_subtree_size = root_inorder_idx - in_start
        return BstNode(
            preorder_sequence[pre_start],
            rebuild_tree_from_preorder_inorder_traversals(
                pre_start + 1, pre_start + 1 + left_subtree_size, in_start,
                root_inorder_idx),
            rebuild_tree_from_preorder_inorder_traversals(
                pre_start + 1 + left_subtree_size, pre_end,
                root_inorder_idx + 1, in_end)
        )

    if len(preorder_sequence) == 0:
        return None
    inorder_sequence: list[int] = sorted(preorder_sequence)
    inorder_idx: dict[int, int] = {value: index for index, value in
                                   enumerate(inorder_sequence)}
    return rebuild_tree_from_preorder_inorder_traversals(
        pre_start=0, pre_end=len(preorder_sequence), in_start=0,
        in_end=len(inorder_sequence))


def rebuild_bst_from_preorder_epi(
        preorder_sequence: list[int]) -> BstNode | None:
    """
    Time complexity = O(n log n) for a balanced BST
                    = O(n ** 2) in the worst case (a left-skewed tree)
                    = O(n) in the best case (a right-skewed tree)
    Space complexity = O(n)

    The worst-case input for this algorithm is the pre-order sequence
    corresponding to a left-skewed tree. The worst-case time complexity
    satisfies the recurrence W(n) = W(n - 1) + O(n), which solves to O(n ** 2).

    The best-case input is a sequence corresponding to a right-skewed tree, and
    the corresponding time complexity is O(n).

    When the sequence corresponds to a balanced BST, the time complexity is
    given by B(n) = 2B(n/2) + O(n), which solves to O(n log n).

    Test PASSED (950/950) [  <1 us]
    Average running time:  364 us
    Median running time:    52 us
    """

    if not preorder_sequence:
        return None

    transition_point = next((i
                             for i, a in enumerate(preorder_sequence)
                             if a > preorder_sequence[0]),
                            len(preorder_sequence))

    return BstNode(
        preorder_sequence[0],
        rebuild_bst_from_preorder_epi(preorder_sequence[1:transition_point]),
        rebuild_bst_from_preorder_epi(preorder_sequence[transition_point:]))


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main(
            'bst_from_preorder.py', 'bst_from_preorder.tsv',
            rebuild_bst_from_preorder))
