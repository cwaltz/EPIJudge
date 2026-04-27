from itertools import accumulate

from test_framework import generic_test


def find_maximum_subarray(nums: list[int]) -> int:
    """
    #16.0

    Time complexity = O(n)
    Space complexity = O(1)

    Using Kadane's algorithm

    Test PASSED (1001/1001) [ 703 us]
    Average running time:    6 us
    Median running time:     2 us
    """
    min_sum = max_sum = running_sum = 0
    for num in nums:
        running_sum += num
        if running_sum < min_sum:
            min_sum = running_sum
        if max_sum < running_sum - min_sum:
            max_sum = running_sum - min_sum
    return max_sum


def find_maximum_subarray_with_itertools_accumulate(nums: list[int]) -> int:
    """
    Test PASSED (1001/1001) [ 695 us]
    Average running time:    6 us
    Median running time:     2 us
    """
    min_sum = max_sum = 0
    for running_sum in accumulate(nums):
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
