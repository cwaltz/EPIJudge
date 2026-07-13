import math

from test_framework import generic_test


def square_root(num: float) -> float:
    """
    #11.5

    Computes the real square root of a floating-point number.

    Time complexity: O(log(num / s)), where s is the tolerance
    Space complexity: O(1)
    """
    # 1. Handle edge cases immediately
    if num < 0:
        raise ValueError("Cannot compute real square root of a negative number")
    if num == 0.0 or num == 1.0:
        return num

    # 2. Determine search boundaries
    # If num < 1.0, the square root is larger than num (e.g., sqrt(0.25) = 0.5)
    # If num > 1.0, the square root is smaller than num (e.g., sqrt(4.0) = 2.0)
    left, right = (num, 1.0) if num < 1.0 else (1.0, num)

    # 3. Binary search with an explicit absolute tolerance
    # An explicit abs_tol prevents infinite loops near zero.
    # while not math.isclose(left, right, rel_tol=1e-9, abs_tol=1e-9):
    while not math.isclose(left, right):
        mid = left + (right - left) / 2.0
        mid_squared = mid * mid

        if mid_squared > num:
            right = mid
        else:
            left = mid

    return left


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('real_square_root.py',
                                       'real_square_root.tsv',
                                       square_root))
