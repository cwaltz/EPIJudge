from typing import List

from test_framework import generic_test


def has_two_sum(nums: List[int], target: int) -> bool:
    """
    #17.0

    Time complexity = O(n), where n is the size of nums.
    Space complexity = O(1)

    Test PASSED (1005/1005) [   4 ms]
    Average running time:   75 us
    Median running time:    11 us
    """
    left, right = 0, len(nums) - 1
    while left <= right:
        if nums[left] + nums[right] == target:
            return True
        if nums[left] + nums[right] < target:
            left += 1
        else:  # target < nums[left] + nums[right]
            right -= 1
    return False


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('two_sum.py', 'two_sum.tsv',
                                       has_two_sum))
