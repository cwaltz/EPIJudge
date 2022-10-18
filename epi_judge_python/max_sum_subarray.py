import itertools
from typing import List

from test_framework import generic_test


def find_maximum_subarray(nums: List[int]) -> int:
    """
    #16.0

    Time complexity = O(n)
    Space complexity = O(1)

    Using Kadane's algorithm

    Test PASSED (1001/1001) [ 902 us]
    Average running time:    8 us
    Median running time:     3 us
    """
    if not nums:
        return 0
    # Empty sub-arrays are acceptable. Hence, initialize curr_sum & max_sum with
    # nums[0] only if nums[0] is positive.
    curr_sum = max_sum = nums[0] if 0 < nums[0] else 0
    # nums[0] has been processed. Start with nums[1].
    for i in range(1, len(nums)):
        # Add curr_sum to nums[i] only if curr_sum is positive.
        curr_sum = nums[i] + (curr_sum if 0 < curr_sum else 0)
        if max_sum < curr_sum:
            max_sum = curr_sum
    return max_sum


def find_maximum_subarray_with_itertools_accumulate(nums: List[int]) -> int:
    """
    Time complexity = O(n)
    Space complexity = O(1)

    Test PASSED (1001/1001) [ 843 us]
    Average running time:    8 us
    Median running time:     3 us
    """
    min_sum = max_sum = 0
    for running_sum in itertools.accumulate(nums):
        if running_sum < min_sum:
            min_sum = running_sum
        if max_sum < running_sum - min_sum:
            max_sum = running_sum - min_sum
    return max_sum


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('max_sum_subarray.py',
                                       'max_sum_subarray.tsv',
                                       find_maximum_subarray))
