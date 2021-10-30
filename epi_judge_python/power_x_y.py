from test_framework import generic_test


def power(x: float, y: int) -> float:
    """The number of multiplications is at most twice the index of y's MSB, implying an O(n) time complexity."""
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
