from typing import List

from test_framework import generic_test


def search_first_of_k(A: List[int], k: int) -> int:
    """
    Time complexity  = O(log n)
    Space complexity = O(1)

    Test PASSED (314/314) [  12 us]
    Average running time:    2 us
    Median running time:     2 us
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
