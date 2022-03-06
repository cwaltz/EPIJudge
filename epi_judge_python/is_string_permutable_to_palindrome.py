from test_framework import generic_test


def can_form_palindrome(s: str) -> bool:
    """
    Test PASSED (305/305) [  29 ms]
    Average running time:   97 us
    Median running time:     2 us
    """

    odd_count = set()
    for c in s:
        if c in odd_count:
            odd_count.remove(c)
        else:
            odd_count.add(c)
    return len(odd_count) < 2


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main(
            'is_string_permutable_to_palindrome.py',
            'is_string_permutable_to_palindrome.tsv', can_form_palindrome))
