from test_framework import generic_test
import string


"""
#6.2

Time complexity = O(n(1 + log_b2 b1)), where n is the length of s.
The reasoning is as follows. First, we perform n multiply-and-adds to get x from s. Then we perform log_b2 x modulus and
division operations to get the result. The value x is upper-bounded by b1 ** n, and log_b2 (b1 ** n) = n log_b2 b1.

Space complexity = O(1)

Test PASSED (20001/20001) [   6 us]
Average running time:    4 us
Median running time:     4 us
"""


def convert_base(num_as_string: str, b1: int, b2: int) -> str:
    if b1 == b2 or num_as_string == '0':
        return num_as_string
    decimal_int = string_to_decimal_int(num_as_string, b1)
    return decimal_int_to_string(decimal_int, b2)


def string_to_decimal_int(s: str, b1: int) -> int:
    num = 0
    if s != '0':
        is_negative = False
        start_index = 0
        if s[0] == '-':
            is_negative = True
            start_index = 1
        for i in range(start_index, len(s)):
            num = num * b1 + string.hexdigits.index(s[i].lower())
        if is_negative:
            num = -num
    return num


def decimal_int_to_string(decimal_int: int, b2: int) -> str:
    is_negative = False
    if decimal_int < 0:
        decimal_int = -decimal_int
        is_negative = True
    result = []
    while True:
        result.append(string.hexdigits[decimal_int % b2].upper())
        decimal_int //= b2
        if decimal_int == 0:
            break
    return ('-' if is_negative else '') + ''.join(reversed(result))


"""
Test PASSED (20001/20001) [   6 us]
Average running time:    5 us
Median running time:     4 us
"""


def convert_base1(s: str, b1: int, b2: int) -> str:
    def to_decimal_int(s: str, b1: int):
        is_negative = False
        start_index = 0
        if s[0] in '+-':
            start_index = 1
            if s[0] == '-':
                is_negative = True
        result = 0
        for i in range(start_index, len(s)):
            result = result * b1 + string.hexdigits.index(s[i].lower())
        return result * -1 if is_negative else result

    def to_base_string(num: int, b2: int):
        if b2 == 10:
            return str(num)
        result = []
        is_negative = False
        if num < 0:
            is_negative = True
            num = -num
        while num:
            result.append(string.hexdigits[num % b2].upper())
            num //= b2
        if is_negative:
            result.append('-')
        return ''.join(reversed(result))

    if b1 == b2 or s == '0':
        return s
    num = to_decimal_int(s, b1)
    return to_base_string(num, b2)


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('convert_base.py', 'convert_base.tsv',
                                       convert_base))
