from test_framework import generic_test


def reverse(x: int) -> int:
    """
    Time complexity  = O(n), where n is the number of digits in x.
    Space complexity = O(1)

    Test PASSED (19952/19952) [   2 us]
    Average running time:    2 us
    Median running time:     2 us
    """
    result, x_remaining = 0, abs(x)
    while x_remaining:
        result = result * 10 + x_remaining % 10
        x_remaining //= 10
    return -result if x < 0 else result


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('reverse_digits.py',
                                       'reverse_digits.tsv', reverse))
