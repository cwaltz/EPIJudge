import bisect
from typing import List

from test_framework import generic_test


# Pythonic solution
def search_first_of_k_pythonic(A, k):
    """
    Test PASSED (314/314) [   3 us]
    Average running time:    1 us
    Median running time:    <1 us
    """
    i = bisect.bisect_left(A, k)
    return i if i < len(A) and A[i] == k else -1


def search_first_of_k(A: List[int], k: int) -> int:
    """
    #11.1

    Time complexity  = O(log n)
    Space complexity = O(1)

    Test PASSED (314/314) [   9 us]
    Average running time:    1 us
    Median running time:     1 us
    """
    result = -1
    left, right = 0, len(A) - 1
    while left <= right:
        mid = left + ((right - left) >> 1)
        if A[mid] < k:
            left = mid + 1
        else:  # k <= A[mid]
            right = mid - 1
            if A[mid] == k:
                result = mid
    return result


def search_first_of_k_1(A: List[int], k: int) -> int:
    """
    Test PASSED (314/314) [  10 us]
    Average running time:    1 us
    Median running time:     1 us
    """
    left, right, result = 0, len(A) - 1, -1
    # A[left:right + 1] is the candidate set.
    while left <= right:
        mid = left + (right - left) // 2
        if A[mid] < k:
            left = mid + 1
        elif A[mid] == k:
            result = mid
            right = mid - 1  # Nothing to the right of mid can be solution.
        else:  # k < A[mid]
            right = mid - 1
    return result


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('search_first_key.py',
                                       'search_first_key.tsv',
                                       search_first_of_k))
