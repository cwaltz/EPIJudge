from typing import List

from test_framework import generic_test


def search_smallest(A: List[int]) -> int:
    """
    Time complexity  = O(log n)
    Space complexity = O(1)

    Note that this problem cannot, in general, be solved in less than linear time when elements may be repeated.
    For example, if A consists of n - 1 1s and a single 0, that 0 cannot be detected in the worst-case without
    inspecting every element.

    Test PASSED (307/307) [   8 us]
    Average running time:    1 us
    Median running time:     1 us
    """

    left, right = 0, len(A) - 1
    while left < right:
        mid = left + (right - left) // 2
        if A[mid] < A[right]:
            # Minimum cannot be in A[mid + 1:right + 1] so it must be in A[left:mid + 1].
            right = mid
        else:  # A[right] < A[mid]
            # Minimum must be in A[mid + 1:right + 1].
            left = mid + 1
    # Loop ends when left == right.
    return left


def search_smallest_v0(A: List[int]) -> int:

    left, right, index = 0, len(A) - 1, len(A) - 1
    smallest_so_far = A[-1]
    while left <= right:
        mid = left + (right - left) // 2
        if A[mid] <= smallest_so_far:
            index, smallest_so_far = mid, A[mid]
            right = mid - 1
        else:  # smallest_so_far < A[mid]
            left = mid + 1
    return index


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('search_shifted_sorted_array.py',
                                       'search_shifted_sorted_array.tsv',
                                       search_smallest))
