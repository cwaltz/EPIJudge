from bst_node import BstNode


# Linear time solutions


def rebuild_bst_from_postorder_iterative(
        postorder_sequence: list[int]) -> BstNode | None:
    """
    #14.5

    Best solution for both - enterprise production environment and software
        engineering interview

    Iteratively reconstructs a BST from a postorder sequence in linear time
    reading right-to-left.

    Time complexity = O(n), n = len(postorder_sequence)
    Space complexity = O(h) on the explicit stack
    """
    if not postorder_sequence:
        return None

    # The last element in postorder is always the root
    root = BstNode(postorder_sequence[-1])
    stack = [root]

    # Iterate backward from the second-to-last element down to index 0
    for i in range(len(postorder_sequence) - 2, -1, -1):
        val = postorder_sequence[i]
        node = BstNode(val)

        # If the value is greater than the top of the stack,
        # it is the right child of the last inserted node.
        if val > stack[-1].data:
            stack[-1].right = node
        else:
            # If the value is smaller, we're moving to a left branch.
            # Pop from the stack to backtrack up the tree until we find
            # the correct parent (the last popped node whose value is greater).
            parent = stack[-1]
            while stack and stack[-1].data > val:
                parent = stack.pop()

            parent.left = node

        # Push the new node onto the stack as it may have children
        stack.append(node)

    return root


def rebuild_bst_from_postorder_recursive(
        postorder_sequence: list[int]) -> BstNode | None:
    """
    Recursively reconstructs a BST from a postorder sequence in linear time
    reading right-to-left.

    Time complexity = O(n)
    Space complexity = O(h) on the function call stack
    """

    def build_subtree(lower_bound: float | int, upper_bound: float | int) -> (
            BstNode | None):
        nonlocal root_idx  # Allows modification of the outer scope integer

        # Stop if we have exhausted the array
        if root_idx < 0:
            return None

        root_val = postorder_sequence[root_idx]

        # Check if the current value belongs in this subtree
        if not (lower_bound <= root_val <= upper_bound):
            return None

        # Consume the node by moving backward through the sequence
        root_idx -= 1

        # CRITICAL: Because we are reading backward, we MUST build the
        # right subtree first, followed by the left subtree.
        right_child = build_subtree(root_val, upper_bound)
        left_child = build_subtree(lower_bound, root_val)

        return BstNode(root_val, left_child, right_child)

    if not postorder_sequence:
        return None

    # Start at the end of the array (the root of the tree)
    root_idx = len(postorder_sequence) - 1
    root = build_subtree(float('-inf'), float('inf'))

    # Production check: ensure no elements were left unprocessed
    if root_idx != -1:
        raise ValueError("Sequence is not a valid postorder traversal.")

    return root
