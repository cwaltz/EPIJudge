import math

from test_framework import generic_test


def square_root(k: int) -> int:
    """
    #11.4

    Time complexity = O(log k)
    Space complexity = O(1)

    Test PASSED (2000/2000) [   5 us]
    Average running time:    3 us
    Median running time:     3 us
    """
    left, right = 0, k
    # Candidate interval [left, right] where everything before left has square <= k,
    # everything after right has square > k.
    while left <= right:
        mid = left + ((right - left) >> 1)
        mid_squared = mid * mid
        if mid_squared <= k:
            left = mid + 1
        else:  # k < mid_squared
            right = mid - 1
    return left - 1


def square_root_pythonic(k: int) -> int:
    """
    Test PASSED (2000/2000) [  <1 us]
    Average running time:   <1 us
    Median running time:    <1 us
    """
    return math.floor(math.sqrt(k))


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('int_square_root.py',
                                       'int_square_root.tsv', square_root))
