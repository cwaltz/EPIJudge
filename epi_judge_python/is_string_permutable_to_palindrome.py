from collections import Counter

from test_framework import generic_test


def can_form_palindrome(s: str) -> bool:
    """
    #12.1

    Time complexity = O(n), where n is the length of the string
    Space complexity = O(c), where c is the number of distinct characters
        appearing in the string.

    Test PASSED (305/305) [  18 ms]
    Average running time:   64 us
    Median running time:     2 us
    """
    letter_frequency = Counter(s)
    odd_frequency = False
    for value in letter_frequency.values():
        if value % 2 == 1:
            if odd_frequency:
                return False
            odd_frequency = True
    return True


def can_form_palindrome_pythonic(s: str) -> bool:
    """
    Test PASSED (305/305) [  18 ms]
    Average running time:   65 us
    Median running time:     2 us
    """
    # A string can be permuted to form a palindrome if and only if the number
    # of chars whose frequencies are odd is at most 1.
    return sum(v % 2 for v in Counter(s).values()) <= 1


def can_form_palindrome_bitwise(s: str) -> bool:
    """
    Checks if a string can be permuted to form a palindrome using bitwise
    operations.

    Test PASSED (305/305) [  60 ms]
    Average running time:  200 us
    Median running time:     1 us
    """
    bit_vector = 0

    for char in s:
        # Create a mask for the character.
        # e.g., 'a' might be bit 97, 'b' bit 98, etc.
        mask = 1 << ord(char)

        # Toggle that specific bit in our vector
        bit_vector ^= mask

    # Check if the bit vector has at most one bit set to 1.
    # The expression (x & (x - 1)) clears the lowest set bit.
    # If the result is 0, it means there was at most one bit set.
    return (bit_vector & (bit_vector - 1)) == 0


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main(
            'is_string_permutable_to_palindrome.py',
            'is_string_permutable_to_palindrome.tsv',
            can_form_palindrome))
