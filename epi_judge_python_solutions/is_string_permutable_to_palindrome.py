import collections

from test_framework import generic_test


def can_form_palindrome(s: str) -> bool:
    """
    The time complexity is O(n), where n is the length of the string. The space complexity is O(c),
    where c is the number of distinct characters appearing in the string.

    Test PASSED (305/305) [  17 ms]
    Average running time:   63 us
    Median running time:     4 us
    """

    # A string can be permuted to form a palindrome if and only if the number
    # of chars whose frequencies is odd is at most 1.
    return sum(v % 2 for v in collections.Counter(s).values()) <= 1


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main(
            'is_string_permutable_to_palindrome.py',
            'is_string_permutable_to_palindrome.tsv', can_form_palindrome))
