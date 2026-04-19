from test_framework import generic_test
from test_framework.test_failure import TestFailure


"""
#6.1

Time complexity = O(n), where n is the length of the string.
Space complexity = O(1)

Test PASSED (15002/15002) [   5 us]
Average running time:    4 us
Median running time:     4 us
"""


def int_to_string_2(x: int) -> str:

    is_negative = False
    if x < 0:
        is_negative, x = True, -x

    result = []
    while True:
        result.append(chr(ord('0') + x % 10))
        x //= 10
        if x == 0:
            break

    # Adds the negative sign back if is_negative
    return ('-' if is_negative else '') + ''.join(reversed(result))


def string_to_int_2(s: str) -> int:

    multiplier = 1
    start_index = 0
    if s[0] in '-+':
        start_index = 1
        if s[0] == '-':
            multiplier = -1

    result = 0
    for i in range(start_index, len(s)):
        result = result * 10 + ord(s[i]) - ord('0')

    return result * multiplier


"""
Test PASSED (15002/15002) [   1 us]
Average running time:    1 us
Median running time:     1 us
"""


def int_to_string_1(x: int) -> str:
    return str(x)


def string_to_int_1(s: str) -> int:
    return int(s)


"""
Test PASSED (15002/15002) [   3 us]
Average running time:    2 us
Median running time:     2 us
"""


def int_to_string(num: int) -> str:
    if num == 0:
        return '0'
    result = []
    is_negative = False
    if num < 0:
        num = -num
        is_negative = True
    ord_0 = ord('0')
    while num > 0:
        digit = num % 10
        num //= 10
        result.append(chr(digit + ord_0))
    if is_negative:
        result.append('-')
    return ''.join(reversed(result))


def string_to_int(s: str) -> int:
    if s == '0':
        return 0
    start = 0
    is_negative = False
    if s[0] in '+-':
        start = 1
        if s[0] == '-':
            is_negative = True
    num = 0
    ord_0 = ord('0')
    for c in s[start:]:
        num = num * 10 + (ord(c) - ord_0)
    return -num if is_negative else num


def wrapper(x, s):
    if int(int_to_string(x)) != x:
        raise TestFailure('Int to string conversion failed')
    if string_to_int(s) != x:
        raise TestFailure('String to int conversion failed')


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('string_integer_interconversion.py',
                                       'string_integer_interconversion.tsv',
                                       wrapper))
