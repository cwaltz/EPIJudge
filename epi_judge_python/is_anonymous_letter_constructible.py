from collections import Counter
from test_framework import generic_test


def is_letter_constructible_from_magazine(letter_text: str,
                                          magazine_text: str) -> bool:
    """
    #12.2

    Time complexity  = O(m + n), where m and n are the number of characters in
        the letter and magazine, respectively.
    Space complexity = O(L), where L is the number of distinct characters
        appearing in the letter.
                     = the size of the hash table constructed in the pass over
                     the letter.

    Test PASSED (212/212) [  13 ms]
    Average running time:   90 us
    Median running time:    15 us
    """
    if not letter_text:
        return True

    if not magazine_text:
        return False

    # Compute the frequencies for all chars in letter_text.
    char_frequency_for_letter: Counter[str] = Counter(letter_text)

    # Checks if characters in magazine_text can cover characters in
    # char_frequency_for_letter.
    for c in magazine_text:
        if c in char_frequency_for_letter:
            char_frequency_for_letter[c] -= 1
            if char_frequency_for_letter[c] == 0:
                del char_frequency_for_letter[c]
                if not char_frequency_for_letter:
                    # All characters for letter_text are matched.
                    return True

    return False


# Pythonic solution that exploits collections.Counter.
# Note that the subtraction only keeps keys with positive counts.
def is_letter_constructible_from_magazine_pythonic(letter_text: str,
                                                   magazine_text: str) -> bool:
    """
    Test PASSED (212/212) [  23 ms]
    Average running time:  134 us
    Median running time:    14 us
    """
    return not Counter(letter_text) - Counter(magazine_text)


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main(
            'is_anonymous_letter_constructible.py',
            'is_anonymous_letter_constructible.tsv',
            is_letter_constructible_from_magazine))
