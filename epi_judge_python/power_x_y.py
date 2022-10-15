import math

from test_framework import generic_test


def power(x: float, y: int) -> float:
    """
    #4.7

    Time complexity  = O(n), where n is number of bits needed to represent y.
    Space complexity = O(1)

    The number of multiplications is at most twice the index of y's MSB,
    implying an O(n) time complexity.

    Test PASSED (10002/10002) [   2 us]
    Average running time:    1 us
    Median running time:     2 us
    """
    result, num = 1.0, y
    if y < 0:
        num = -num
        x = 1 / x
    while num:
        # if num & 1:
        if num % 2:  # Might be faster than: num & 1
            result *= x
        num >>= 1
        x = x * x
    return result


def power_direct(x: float, y: int) -> float:
    """
    Test PASSED (10002/10002) [  <1 us]
    Average running time:   <1 us
    Median running time:    <1 us
    """
    return x ** y


def power_using_math_pow(x: float, y: int) -> float:
    """
    Test PASSED (10002/10002) [  <1 us]
    Average running time:   <1 us
    Median running time:    <1 us
    """
    return math.pow(x, y)


if __name__ == '__main__':
    exit(generic_test.generic_test_main('power_x_y.py', 'power_x_y.tsv',
                                        power))
