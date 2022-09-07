import collections

from test_framework import generic_test


def can_form_palindrome_pythonic(s: str) -> bool:
    """
    #12.1

    Time complexity = O(n), where n is the length of the string.
    Space complexity = O(c), where c is the number of distinct characters appearing in the string.

    Test PASSED (305/305) [  21 ms]
    Average running time:   73 us
    Median running time:     3 us
    """
    # A string can be permuted to form a palindrome if and only if the number
    # of chars whose frequencies are odd is at most 1.
    return sum(v % 2 for v in collections.Counter(s).values()) <= 1


def can_form_palindrome(s: str) -> bool:
    """
    Test PASSED (305/305) [  21 ms]
    Average running time:   72 us
    Median running time:     3 us
    """
    letter_frequency: collections.Counter[str, int] = collections.Counter(s)
    odd_frequency = False
    for value in letter_frequency.values():
        if value % 2 == 1:
            if odd_frequency:
                return False
            odd_frequency = True
    return True


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main(
            'is_string_permutable_to_palindrome.py',
            'is_string_permutable_to_palindrome.tsv', can_form_palindrome))
