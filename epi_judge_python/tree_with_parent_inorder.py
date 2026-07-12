from binary_tree_with_parent_prototype import BinaryTreeNode
from test_framework import generic_test


def inorder_traversal(tree: BinaryTreeNode) -> list[int]:
    """
    #9.11

    Time complexity = O(n), n = # of nodes in the tree
    Space complexity = O(1)

    Test PASSED (3852/3852) [  <1 us]
    Average running time:   11 us
    Median running time:     1 us
    """
    if not tree:
        return []

    result = []
    curr = tree
    prev = None

    while curr:
        if prev is curr.parent:
            if curr.left:
                next_node = curr.left
            else:
                result.append(curr.data)
                next_node = curr.right or curr.parent
        elif prev is curr.left:
            result.append(curr.data)
            next_node = curr.right or curr.parent
        else:  # elif prev is curr.right:
            next_node = curr.parent

        prev = curr
        curr = next_node

    return result


def inorder_traversal_iterative_linear_space(tree: BinaryTreeNode) -> list[int]:
    """
    Time complexity = O(n), n = # of nodes in the tree
    Space complexity = O(n)

    Test PASSED (3852/3852) [  <1 us]
    Average running time:    9 us
    Median running time:     1 us
    """
    result = []
    stack = []
    curr = tree

    while curr or stack:
        # 1. Dive as far left as possible
        while curr:
            stack.append(curr)
            curr = curr.left

        # 2. Process the node at the bottom left
        curr = stack.pop()
        result.append(curr.data)

        # 3. Move to the right child and repeat
        curr = curr.right

    return result


def inorder_traversal_recursive_linear_space(tree: BinaryTreeNode) -> list[int]:
    """
    Time complexity = O(n), n = # of nodes in the tree
    Space complexity = O(n)

    Test PASSED (3852/3852) [  <1 us]
    Average running time:   10 us
    Median running time:     1 us
    """
    def inorder_traversal_helper(node: BinaryTreeNode) -> None:
        if not node:
            return

        inorder_traversal_helper(node.left)
        result.append(node.data)
        inorder_traversal_helper(node.right)

    result = []
    inorder_traversal_helper(tree)
    return result


def inorder_traversal_recursive_alternate(tree: BinaryTreeNode) -> list[int]:
    """
    This non-idiomatic version runs faster and is more efficient than
    inorder_traversal_recursive_linear_space(). BUT, the
    inorder_traversal_recursive_linear_space() is the recommended standard in
    the industry due to being idiomatic, simpler and bulletproof.

    Time complexity = O(n), n = # of nodes in the tree
    Space complexity = O(n)

    Test PASSED (3852/3852) [  <1 us]
    Average running time:    7 us
    Median running time:     1 us
    """
    def inorder_traversal_helper(node: BinaryTreeNode) -> None:
        if node.left:
            inorder_traversal_helper(node.left)
        result.append(node.data)
        if node.right:
            inorder_traversal_helper(node.right)

    if not tree:
        return []

    result = []
    inorder_traversal_helper(tree)
    return result


def inorder_traversal_iterative_alternate(tree: BinaryTreeNode) -> list[int]:
    """
    Time complexity = O(n), n = # of nodes in the tree
    Space complexity = O(n)

    Test PASSED (3852/3852) [  <1 us]
    Average running time:   16 us
    Median running time:     2 us
    """
    if not tree:
        return []

    result = []
    stack = [(tree, False)]
    # The boolean value indicates whether the left child has been visited

    while stack:
        node, left_visited = stack.pop()
        if left_visited:
            result.append(node.data)
            if node.right:
                stack.append((node.right, False))
        else:
            stack.append((node, True))
            if node.left:
                stack.append((node.left, False))

    return result


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('tree_with_parent_inorder.py',
                                       'tree_with_parent_inorder.tsv',
                                       inorder_traversal))
