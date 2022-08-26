from binary_tree_node import BinaryTreeNode

"""
#9.0

Time complexity = O(n), where n is the number of nodes in the tree.
Space complexity = O(h), where h is the height of the tree.

Binary trees boot camp

A good way to get up to speed with binary trees is to implement the three basic traversals - inorder, preorder,
and postorder.

The time complexity of each approach is O(n), where n is the number of nodes in the tree. Although no memory is
explicitly allocated, the function call stack reaches a maximum depth of h, the height of the tree. Therefore, the space
complexity is O(h). The minimum value for h is log n (complete binary tree) and the maximum value for h is n (skewed
tree).
"""


def tree_traversal(root: BinaryTreeNode) -> None:
    if root:
        # Preorder: Processes the root before the traversals of left and right children.
        print('Preorder: %d' % root.data)
        tree_traversal(root.left)
        # Inorder: Processes the root after the traversal of left child and before the traversal of right child.
        print('Inorder: %d' % root.data)
        tree_traversal(root.right)
        # Postorder: Processes the root after the traversals of left and right children.
        print('Postorder: %d' % root.data)
