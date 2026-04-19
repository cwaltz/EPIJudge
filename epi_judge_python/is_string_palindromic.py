from test_framework import generic_test


def is_palindromic(s: str) -> bool:
    """
    #6.0

    Time complexity = O(n), where n is the length of the string.
    Space complexity = O(1)

    Test PASSED (10000/10000) [   1 us]
    Average running time:    1 us
    Median running time:     1 us
    """
    # Note that s[~i] for i in [0, len(s) - 1] is s[-(i + 1)].
    return all(s[i] == s[~i] for i in range(len(s) // 2))


def is_palindromic_pythonic(s: str) -> bool:
    """
    Test PASSED (10000/10000) [  <1 us]
    Average running time:   <1 us
    Median running time:    <1 us
    """
    return s == s[::-1]


def is_palindromic_1(s: str) -> bool:
    """
    Test PASSED (10000/10000) [  <1 us]
    Average running time:   <1 us
    Median running time:    <1 us
    """
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1

    return True


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('is_string_palindromic.py',
                                       'is_string_palindromic.tsv',
                                       is_palindromic))
