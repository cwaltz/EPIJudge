from test_framework import generic_test


def power(x: float, y: int) -> float:
    """
    Time complexity  = O(n), where n is number of bits needed to represent y.
    Space complexity = O(1)

    The number of multiplications is at most twice the index of y's MSB, implying an O(n) time complexity.

    Test PASSED (10002/10002) [   3 us]
    Average running time:    3 us
    Median running time:     3 us
    """
    result, num = 1.0, y
    if y < 0:
        num = -num
        x = 1 / x
    while num:
        if num & 1:
            result *= x
        num >>= 1
        x = x * x
    return result


if __name__ == '__main__':
    exit(generic_test.generic_test_main('power_x_y.py', 'power_x_y.tsv',
                                        power))
