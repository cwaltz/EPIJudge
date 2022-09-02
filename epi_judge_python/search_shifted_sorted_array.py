from typing import List

from test_framework import generic_test


def search_smallest(A: List[int]) -> int:
    """
    #11.3

    Time complexity  = O(log n)
    Space complexity = O(1)

    Note that this problem cannot, in general, be solved in less than linear time when elements may be repeated.
    For example, if A consists of n - 1 1s and a single 0, that 0 cannot be detected in the worst-case without
    inspecting every element.

    Test PASSED (307/307) [   4 us]
    Average running time:    1 us
    Median running time:     1 us
    """
    left, right = 0, len(A) - 1
    while left < right:
        mid = (left + right) // 2
        if A[mid] > A[right]:
            # Minimum must be in A[mid + 1:right + 1].
            left = mid + 1
        else:  # A[mid] < A[right].
            # Minimum cannot be in A[mid + 1:right + 1] so it must be in A[left:mid + 1].
            right = mid
    # Loop ends when left == right.
    return left


def search_smallest_simpler(A: List[int]) -> int:
    """
    Test PASSED (307/307) [   5 us]
    Average running time:    1 us
    Median running time:     1 us
    """
    # All elements are distinct.
    if len(A) == 1 or A[0] < A[-1]:
        return 0
    left, right, result = 0, len(A) - 1, len(A) - 1
    while left <= right:
        mid = left + ((right - left) >> 1)
        if A[mid] < A[result]:
            result = mid
            right = mid - 1
        else:  # A[result] < A[mid]
            left = mid + 1
    return result


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('search_shifted_sorted_array.py',
                                       'search_shifted_sorted_array.tsv',
                                       search_smallest))
