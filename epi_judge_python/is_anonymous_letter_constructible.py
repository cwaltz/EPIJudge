import collections
from test_framework import generic_test


def is_letter_constructible_from_magazine(letter_text: str,
                                          magazine_text: str) -> bool:
    if not letter_text:
        return True
    letter_frequency = collections.Counter(letter_text)
    for c in magazine_text:
        if c in letter_frequency:
            letter_frequency[c] -= 1
            if letter_frequency[c] == 0:
                del letter_frequency[c]
                if not letter_frequency:
                    return True
    return False


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main(
            'is_anonymous_letter_constructible.py',
            'is_anonymous_letter_constructible.tsv',
            is_letter_constructible_from_magazine))
