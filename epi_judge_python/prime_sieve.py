"""
#5.9

For all 3 versions, complexity analysis is as follows:

Time complexity = O(n log log n)
Space complexity = O(n)

generate_primes(n): This is the perfect baseline for a coding interview.
It shows you understand the standard Sieve of Eratosthenes. It is readable,
easy to trace, and easy to write on a whiteboard without making off-by-1 errors.

generate_primes_fast(n): While this demonstrates a deep understanding of memory
optimization (stripping out even numbers cuts the space in half), writing this
in a live interview is risky. The index math 2 * (i ** 2) + 6 * i + 3 is highly
error-prone under pressure. In an interview, it is often better to write the
basic version, explain the p ** 2 inner-loop optimization, and verbally discuss
the "skip evens" optimization rather than writing it out.

generate_primes_pythonic(n): The "Pythonic" Way (Slice Assignment): Python for
loops are relatively slow in CPython. In production, if you must write your own
sieve in Python, list slice assignments are significantly faster because they
push the loop down into C.
"""

from test_framework import generic_test


def generate_primes(n: int) -> list[int]:
    """
    Test PASSED (24/24) [ 118 ms]
    Average running time:    5 ms
    Median running time:     2 us
    """
    primes = []

    # is_prime[p] represents if p is prime or not. Initially, set each to True,
    # except 0 and 1. Then use sieving to eliminate nonprimes.
    is_prime = [False, False] + [True] * (n - 1)
    for p in range(2, n + 1):
        if is_prime[p]:
            primes.append(p)
            # Sieve p's multiples.
            for multiple in range(p ** 2, n + 1, p):
                is_prime[multiple] = False

    return primes


def generate_primes_fast(n: int) -> list[int]:
    """
    Test PASSED (24/24) [  68 ms]
    Average running time:    3 ms
    Median running time:     2 us
    """

    if n < 2:
        return []
    size = (n - 1) // 2
    primes = [2]  # Stores the primes from 1 to n.
    # is_prime[i] represents (2 * i + 3) is prime or not.
    # For example,
    # is_prime[0] represents 3 is prime or not,
    # is_prime[1] represents 5,
    # is_prime[2] represents 7, etc.
    # Initially set each to true. Then use sieving to eliminate nonprimes.
    is_prime = [True] * size
    for i in range(size):
        if is_prime[i]:
            p = 2 * i + 3
            primes.append(p)
            # Sieving from p ** 2, where p ** 2 = (4 * (i ** 2) + 12 * i + 9).
            # The index in is_prime is (2 * (i ** 2) + 6 * i + 3)
            # because is_prime[i] represents 2 * i + 3.
            for j in range(2 * (i ** 2) + 6 * i + 3, size, p):
                is_prime[j] = False

    return primes


def generate_primes_pythonic(n: int) -> list[int]:
    """
    Test PASSED (24/24) [  60 ms]
    Average running time:    2 ms
    Median running time:     2 us
    """
    if n < 2:
        return []
    sieve = [True] * (n + 1)
    for p in range(2, int(n ** 0.5) + 1):
        if sieve[p]:
            # Slice assignment is much faster than a standard for-loop
            sieve[p * p: n + 1: p] = [False] * len(sieve[p * p: n + 1: p])
    return [p for p, is_prime in enumerate(sieve) if is_prime and p >= 2]


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('prime_sieve.py',
                                       'prime_sieve.tsv',
                                       generate_primes))
