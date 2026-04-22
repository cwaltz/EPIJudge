import bisect

from test_framework import generic_test


def intersect_two_sorted_arrays(first: list[int], second: list[int]) \
        -> list[int]:
    """
    #13.1

    Time complexity = O(m + n) where m = len(A) and n = len(B)
    Space complexity = O(1)

    Test PASSED (202/202) [   6 ms]
    Average running time:   36 us
    Median running time:     2 us
    """
    i, j, result = 0, 0, []
    len_a, len_b = len(first), len(second)
    while i < len_a and j < len_b:
        # Faster than using len(A) & len(B) instead of len_a & len_b
        if first[i] == second[j]:
            if i == 0 or first[i] != first[i - 1]:
                result.append(first[i])
            i, j = i + 1, j + 1
        elif first[i] < second[j]:
            i += 1
        else:  # second[j] < first[i]
            j += 1
    return result


def intersect_two_sorted_arrays_using_binary_search(
        first: list[int], second: list[int]) -> list[int]:
    """
    Time complexity = O(m log n),
        m = length of smaller array and n = length of larger array
    Space complexity = O(1)

    Test PASSED (202/202) [  10 ms]
    Average running time:   55 us
    Median running time:     2 us
    """
    def is_present(nums: list[int], a: int) -> bool:
        i = bisect.bisect_left(nums, a)
        return i < len(nums) and a == nums[i]

    if len(first) < len(second):
        return [a for i, a in enumerate(first)
                if (i == 0 or a != first[i - 1]) and is_present(second, a)]
    else:  # len(second) < len(first)
        return [b for j, b in enumerate(second)
                if (j == 0 or b != second[j - 1]) and is_present(first, b)]


def intersect_two_sorted_arrays_pythonic(first: list[int], second: list[int]) \
        -> list[int]:
    """
    Time complexity = O(m * n) where m = len(A) and n = len(B)
    Space complexity = O(1)

    Test PASSED (202/202) [   5  s]
    Average running time:   28 ms
    Median running time:     3 us
    """
    return [a for i, a in enumerate(first)
            if (i == 0 or a != first[i - 1]) and a in second]


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('intersect_sorted_arrays.py',
                                       'intersect_sorted_arrays.tsv',
                                       intersect_two_sorted_arrays))
