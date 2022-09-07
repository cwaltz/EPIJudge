from typing import List

from test_framework import generic_test


def merge_two_sorted_arrays(A: List[int], m: int, B: List[int],
                            n: int) -> None:
    """
    #13.2

    Time complexity = O(m + n), where m and n are the number of entries initially in the first and second arrays.
    Space complexity = O(1)

    Test PASSED (201/201) [   6 ms]
    Average running time:   40 us
    Median running time:     4 us
    """
    i, j, write_idx = m - 1, n - 1, m + n - 1
    while i >= 0 and j >= 0:
        if A[i] < B[j]:
            A[write_idx] = B[j]
            j -= 1
        else:  # B[j] <= A[i]
            A[write_idx] = A[i]
            i -= 1
        write_idx -= 1
    if j >= 0:
        A[:j + 1] = B[:j + 1]


def merge_two_sorted_arrays_wrapper(A, m, B, n):
    merge_two_sorted_arrays(A, m, B, n)
    return A


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('two_sorted_arrays_merge.py',
                                       'two_sorted_arrays_merge.tsv',
                                       merge_two_sorted_arrays_wrapper))
