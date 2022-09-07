import bisect
from typing import List

from test_framework import generic_test


def intersect_two_sorted_arrays(A: List[int], B: List[int]) -> List[int]:
    """
    #13.1

    Time complexity = O(m + n) where m = len(A) and n = len(B)
    Space complexity = O(1)

    Test PASSED (202/202) [   8 ms]
    Average running time:   50 us
    Median running time:     3 us
    """
    i, j, result = 0, 0, []
    len_a, len_b = len(A), len(B)
    while i < len_a and j < len_b:  # Faster than using len(A) & len(B) instead of len_a & len_b
        if A[i] == B[j]:
            if i == 0 or A[i] != A[i - 1]:
                result.append(A[i])
            i, j = i + 1, j + 1
        elif A[i] < B[j]:
            i += 1
        else:  # B[j] < A[i]
            j += 1
    return result


def intersect_two_sorted_arrays_using_binary_search(A: List[int], B: List[int]) -> List[int]:
    """
    Time complexity = O(m log n) where m = length of smaller array and n = length of larger array
    Space complexity = O(1)

    Test PASSED (202/202) [  15 ms]
    Average running time:   85 us
    Median running time:     5 us
    """
    def is_present(nums: List[int], a: int) -> bool:
        i = bisect.bisect_left(nums, a)
        return i < len(nums) and a == nums[i]

    if len(A) < len(B):
        return [a for i, a in enumerate(A) if (i == 0 or a != A[i - 1]) and is_present(B, a)]
    else:  # len(B) < len(A)
        return [b for j, b in enumerate(B) if (j == 0 or b != B[j - 1]) and is_present(A, b)]


def intersect_two_sorted_arrays_pythonic(A: List[int], B: List[int]) -> List[int]:
    """
    Time complexity = O(m * n) where m = len(A) and n = len(B)
    Space complexity = O(1)

    Test PASSED (202/202) [   5  s]
    Average running time:   28 ms
    Median running time:     3 us
    """
    return [a for i, a in enumerate(A) if (i == 0 or a != A[i - 1]) and a in B]


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('intersect_sorted_arrays.py',
                                       'intersect_sorted_arrays.tsv',
                                       intersect_two_sorted_arrays))
