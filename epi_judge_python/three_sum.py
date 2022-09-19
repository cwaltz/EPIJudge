from typing import List

from test_framework import generic_test
from two_sum import has_two_sum


def has_three_sum(nums: List[int], target: int) -> bool:
    """
    #17.4

    Time complexity = O(n ** 2), where n is the length of the array.
    Space complexity = O(1)

    Test PASSED (1008/1008) [   3  s]
    Average running time:    3 ms
    Median running time:    10 us
    """
    def has_two_sum(left: int, right: int, target: int) -> bool:
        while left <= right:
            if nums[left] + nums[right] == target:
                return True
            if nums[left] + nums[right] < target:
                left += 1
            else:  # target < nums[left] + nums[right]
                right -= 1
        return False

    nums.sort()
    n = len(nums)
    for i in range(n):
        if has_two_sum(i, n - 1, target - nums[i]):
            return True
    return False


def has_three_sum_shorter(A: List[int], t: int) -> bool:
    """
    Test PASSED (1008/1008) [   3  s]
    Average running time:    4 ms
    Median running time:    11 us
    """
    A.sort()
    # Finds if the sum of two numbers in A equals to t - a.
    return any(has_two_sum(A, t - a) for a in A)


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('three_sum.py', 'three_sum.tsv',
                                       has_three_sum))
