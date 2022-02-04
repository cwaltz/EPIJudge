from test_framework import generic_test
from test_framework.test_failure import TestFailure


def int_to_string(x: int) -> str:

    is_negative = False
    if x < 0:
        is_negative, x = True, -x

    result = []
    while True:
        result.append(chr(ord('0') + x % 10))
        x //= 10
        if x == 0:
            break

    return ('-' if is_negative else '') + ''.join(reversed(result))


def string_to_int(s: str) -> int:

    multiplier = 1
    start_index = 0
    if s[0] in '-+':
        start_index = 1
        if s[0] == '-':
            multiplier = -1

    result = 0
    for i in range(start_index, len(s)):
        result *= 10
        result += int(s[i])

    return result * multiplier


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
