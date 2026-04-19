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
    left, right, result = 0, k, 0
    while left <= right:
        mid = left + ((right - left) >> 1)
        mid_squared = mid * mid
        if mid_squared == k:
            return mid
        elif mid_squared < k:
            result = mid
            left = mid + 1
        else:  # k < mid_squared
            right = mid - 1
    return result


def square_root_faster(k: int) -> int:
    """
    Test PASSED (2000/2000) [   4 us]
    Average running time:    2 us
    Median running time:     2 us
    """
    left, right = 0, k
    # Candidate interval [left, right] where everything before left has
    # square <= k, everything after right has square > k.
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


def square_root_pocket_calculator_algorithm(k: int) -> int:
    """
    Time complexity = O(1)
    Space complexity = O(1)

    Test PASSED (2000/2000) [   1 us]
    Average running time:    1 us
    Median running time:     1 us
    """
    if k < 2:
        return k
    left = int(math.e ** (0.5 * math.log(k)))
    right = left + 1
    return left if right * right > k else right


def square_root_recursion_and_bit_shifts(k: int) -> int:
    """
    Time complexity = O(log k)
    Space complexity = O(log k)

    Test PASSED (2000/2000) [   4 us]
    Average running time:    2 us
    Median running time:     2 us
    """
    if k < 2:
        return k
    left = square_root_recursion_and_bit_shifts(k >> 2) << 1
    right = left + 1
    return left if right * right > k else right


def square_root_newtons_method(x: int) -> int:
    """
    Time complexity = O(log x)
    Space complexity = O(1)

    Test PASSED (2000/2000) [   3 us]
    Average running time:    2 us
    Median running time:     2 us
    """
    if x < 2:
        return x
    prev_root = x
    root = (prev_root + x / prev_root) / 2
    while abs(prev_root - root) >= 1:
        prev_root = root
        root = (prev_root + x / prev_root) / 2

    return int(root)


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('int_square_root.py',
                                       'int_square_root.tsv', square_root))
