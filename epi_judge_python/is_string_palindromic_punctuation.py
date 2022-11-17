from test_framework import generic_test


def is_palindrome(s: str) -> bool:
    """
    #6.5

    Similar to Leetcode # 125. Valid Palindrome

    Time complexity = O(n), where n is the length of the string.
    Space complexity = O(1)

    Test PASSED (305/305) [  47 ms]
    Average running time:  156 us
    Median running time:     1 us
    """
    # left moves forward, and right moves backward.
    left, right = 0, len(s) - 1
    while left < right:
        # left and right both skip non-alphanumeric characters.
        while not s[left].isalnum() and left < right:
            left += 1
        while not s[right].isalnum() and left < right:
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main(
            'is_string_palindromic_punctuation.py',
            'is_string_palindromic_punctuation.tsv', is_palindrome))
