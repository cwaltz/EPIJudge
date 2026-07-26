from collections.abc import Sequence

from test_framework import generic_test


def get_max_trapped_water(heights: Sequence[int]) -> int:
    """
    #17.7

    Sequence[int] from collections.abc allows the function to accept tuples or
    other sequence types without complaining

    Time complexity = O(n), n = len(heights)
    Space complexity = O(1)

    Test PASSED (204/204) [   4 ms]
    Average running time:   77 us
    Median running time:     6 us
    """

    max_amount = 0
    i, j = 0, len(heights) - 1
    while i < j:
        curr_amount = min(heights[i], heights[j]) * (j - i)

        if max_amount < curr_amount:
            max_amount = curr_amount

        # Move the pointer pointing to the shorter line
        if heights[i] < heights[j]:
            i += 1
        else:  # elif heights[j] <= heights[i]:
            j -= 1

    return max_amount


def get_max_trapped_water_epi(heights: list[int]) -> int:
    """
    Test PASSED (204/204) [   4 ms]
    Average running time:   90 us
    Median running time:     7 us
    """

    i, j, max_water = 0, len(heights) - 1, 0
    while i < j:
        max_water = max(max_water, (j - i) * min(heights[i], heights[j]))
        if heights[i] > heights[j]:
            j -= 1
        else:  # heights[i] <= heights[j].
            i += 1
    return max_water


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('max_trapped_water.py',
                                       'max_trapped_water.tsv',
                                       get_max_trapped_water))
