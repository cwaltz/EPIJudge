"""
#12.0

Now we illustrate the steps for designing a hash function suitable for strings.
First, the hash function should examine all the characters in the string. It
should give a large range of values, and should not let one character dominate
(e.g., if we simply cast characters to integers and multiplied them, a single 0
would result in a hash code of 0). We would also like a rolling hash function,
one in which if a character is deleted from the front of the string, and
another added to the end, the new hash code can be computed in O(1) time. The
following function has these properties:
"""

import functools
from typing import List


def string_hash(s: str, modulus: int) -> int:
    MULT = 997
    hash_value = 0

    for char in s:
        # 1. Multiply current hash by the multiplier
        # 2. Add the integer value of the character
        # 3. Take the modulo to prevent the number from getting too large
        hash_value = (hash_value * MULT + ord(char)) % modulus

    return hash_value


def string_hash_pythonic(s: str, modulus: int) -> int:
    MULT = 997
    return functools.reduce(lambda v, c: (v * MULT + ord(c)) % modulus, s, 0)


def rabin_karp_search(text: str, pattern: str) -> List[int]:
    """
    Explanation: https://gemini.google.com/app/1bd3e85573324ac5
    """
    n, m = len(text), len(pattern)
    if m == 0 or n < m:
        return []

    MULT = 997
    MODULUS = 10 ** 9 + 7

    # 1. Precalculate MULT^(m-1) % MODULUS
    # We use Python's built-in pow() which does modular exponentiation
    # efficiently
    MULT_POW = pow(MULT, m - 1, MODULUS)

    # 2. Calculate the initial hashes for the pattern and the first window of
    # text
    pattern_hash = 0
    window_hash = 0
    for i in range(m):
        pattern_hash = (pattern_hash * MULT + ord(pattern[i])) % MODULUS
        window_hash = (window_hash * MULT + ord(text[i])) % MODULUS

    results = []

    # 3. Slide the window over the text
    for i in range(n - m + 1):
        # If hashes match, verify the actual strings to avoid hash collisions
        if window_hash == pattern_hash:
            if text[i: i + m] == pattern:
                results.append(i)

        # Update the rolling hash for the next window
        if i < n - m:
            char_out = ord(text[i])
            char_in = ord(text[i + m])

            # Remove outgoing, multiply by MULT, add incoming
            window_hash = ((window_hash - char_out * MULT_POW) * MULT +
                           char_in) % MODULUS

            # Pro-Tip: In Python, modulo of a negative number is positive.
            # In languages like C++ or Java, you must force it to be positive:
            # window_hash = (window_hash % MODULUS + MODULUS) % MODULUS

    return results
