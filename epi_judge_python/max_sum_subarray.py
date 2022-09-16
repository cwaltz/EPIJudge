import itertools
from typing import List

from test_framework import generic_test


def find_maximum_subarray(nums: List[int]) -> int:
    """
    #16.0

    Time complexity = O(n)
    Space complexity = O(1)

    Test PASSED (1001/1001) [ 931 us]
    Average running time:    9 us
    Median running time:     3 us
    """
    running_sum = max_sum = min_sum = 0
    for num in nums:
        running_sum += num
        if running_sum < min_sum:
            min_sum = running_sum
        if max_sum < running_sum - min_sum:
            max_sum = running_sum - min_sum
    return max_sum


def find_maximum_subarray_with_itertools_accumulate(nums: List[int]) -> int:
    """
    Time complexity = O(n)
    Space complexity = O(1)

    Test PASSED (1001/1001) [ 907 us]
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
