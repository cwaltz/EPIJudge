import bisect
from typing import List

from test_framework import generic_test


def search_first_of_k(nums: List[int], k: int) -> int:
    """
    #11.1

    Time complexity  = O(log n)
    Space complexity = O(1)

    Test PASSED (314/314) [   4 us]
    Average running time:    1 us
    Median running time:     1 us
    """
    result = -1
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = left + ((right - left) >> 1)
        if nums[mid] < k:
            left = mid + 1
        else:  # k <= A[mid]
            right = mid - 1
            if nums[mid] == k:
                result = mid
    return result


def search_first_of_k_1(nums: List[int], k: int) -> int:
    """
    Test PASSED (314/314) [   4 us]
    Average running time:    1 us
    Median running time:     1 us
    """
    left, right, result = 0, len(nums) - 1, -1
    # A[left:right + 1] is the candidate set.
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] < k:
            left = mid + 1
        elif nums[mid] == k:
            result = mid
            right = mid - 1  # Nothing to the right of mid can be solution.
        else:  # k < A[mid]
            right = mid - 1
    return result


# Pythonic solution
def search_first_of_k_pythonic(nums: List[int], k: int) -> int:
    """
    Test PASSED (314/314) [   1 us]
    Average running time:   <1 us
    Median running time:    <1 us
    """
    i = bisect.bisect_left(nums, k)
    return i if i < len(nums) and nums[i] == k else -1


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('search_first_key.py',
                                       'search_first_key.tsv',
                                       search_first_of_k))
