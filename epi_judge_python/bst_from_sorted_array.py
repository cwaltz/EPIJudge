import functools
from typing import List, Optional

from bst_node import BstNode
from test_framework import generic_test
from test_framework.binary_tree_utils import (binary_tree_height,
                                              generate_inorder)
from test_framework.test_failure import TestFailure
from test_framework.test_utils import enable_executor_hook


def build_min_height_bst_from_sorted_array(nums: List[int]) -> Optional[BstNode]:
    """
    #14.8

    Time complexity = O(n)
    Space complexity = O(log n) on function call stack.

    The time complexity T(n) satisfies the recurrence T(n) = 2T(n/2) + O(1),
    which solves to T(n) = O(n). Another explanation for the time complexity
    is that we make exactly n calls to the recursive function and spend O(1)
    within each call.

    Test PASSED (87/87) [   7 us]
    Average running time:   24 us
    Median running time:    12 us
    """

    def build_min_height_bst_from_sorted_subarray(start, end):
        if end <= start:
            return None
        mid = start + ((end - start) >> 1)
        return BstNode(
            nums[mid],
            build_min_height_bst_from_sorted_subarray(start, mid),
            build_min_height_bst_from_sorted_subarray(mid + 1, end)
        )

    return build_min_height_bst_from_sorted_subarray(0, len(nums))


@enable_executor_hook
def build_min_height_bst_from_sorted_array_wrapper(executor, A):
    result = executor.run(
        functools.partial(build_min_height_bst_from_sorted_array, A))

    if generate_inorder(result) != A:
        raise TestFailure('Result binary tree mismatches input array')
    return binary_tree_height(result)


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main(
            'bst_from_sorted_array.py', 'bst_from_sorted_array.tsv',
            build_min_height_bst_from_sorted_array_wrapper))
