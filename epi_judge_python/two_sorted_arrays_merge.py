from test_framework import generic_test


def merge_two_sorted_arrays(first: list[int], m: int, second: list[int],
                            n: int) -> None:
    """
    #13.2

    Time complexity = O(m + n), where m and n are the number of entries
        initially in the first and second arrays.
    Space complexity = O(1)

    Test PASSED (201/201) [   5 ms]
    Average running time:   32 us
    Median running time:     2 us
    """
    i, j, write_idx = m - 1, n - 1, m + n - 1
    while i >= 0 and j >= 0:
        if first[i] < second[j]:
            first[write_idx] = second[j]
            j -= 1
        else:  # second[j] <= first[i]
            first[write_idx] = first[i]
            i -= 1
        write_idx -= 1
    if j >= 0:
        first[:j + 1] = second[:j + 1]


def merge_two_sorted_arrays_wrapper(first: list[int], m: int, second: list[int],
                                    n: int) -> list[int]:
    merge_two_sorted_arrays(first, m, second, n)
    return first


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('two_sorted_arrays_merge.py',
                                       'two_sorted_arrays_merge.tsv',
                                       merge_two_sorted_arrays_wrapper))
