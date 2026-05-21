from test_framework import generic_test


def reverse_digits(num: int) -> int:
    if -9 <= num <= 9:
        return num

    multiplier = 1
    if num < 0:
        multiplier, num = -1, -num

    result = 0
    while num:
        result = result * 10 + num % 10
        num //= 10

    return result * multiplier


def reverse(x: int) -> int:
    """
    #4.8

    Time complexity  = O(n), where n is the number of digits in x.
    Space complexity = O(1)

    Test PASSED (19952/19952) [  <1 us]
    Average running time:    1 us
    Median running time:     1 us
    """
    result, x_remaining = 0, abs(x)
    while x_remaining:
        result = result * 10 + x_remaining % 10
        x_remaining //= 10
    return -result if x < 0 else result


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('reverse_digits.py',
                                       'reverse_digits.tsv',
                                       reverse_digits))
