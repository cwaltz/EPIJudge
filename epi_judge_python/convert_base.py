from test_framework import generic_test
import string


def convert_base(num_as_string: str, b1: int, b2: int) -> str:
    if b1 == b2:
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


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('convert_base.py', 'convert_base.tsv',
                                       convert_base))
