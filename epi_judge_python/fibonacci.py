from functools import cache, lru_cache

from test_framework import generic_test


@cache
def fibonacci(n: int) -> int:
    """
    #16.0

    Time complexity = O(n)
    Space complexity = O(n) due to caching.

    Test PASSED (46/46) [  <1 us]
    Average running time:   <1 us
    Median running time:    <1 us
    """
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


@lru_cache(maxsize=None)
# maxsize is set to None, the LRU feature is disabled & the cache can grow
# without bound.
def fibonacci_1(n: int) -> int:
    """
    Test PASSED (46/46) [  <1 us]
    Average running time:   <1 us
    Median running time:    <1 us
    """
    if n <= 1:
        return n
    return fibonacci_1(n - 1) + fibonacci_1(n - 2)


def fibonacci_constant_space(n: int) -> int:
    """
    Time complexity = O(n)
    Space complexity = O(1)

    Test PASSED (46/46) [   2 us]
    Average running time:    1 us
    Median running time:     1 us
    """
    if n < 2:
        return n
    f_minus_2, f_minus_1 = 0, 1
    for _ in range(n - 1):
        # f = f_minus_2 + f_minus_1
        # f_minus_2, f_minus_1 = f_minus_1, f
        f_minus_2, f_minus_1 = f_minus_1, f_minus_2 + f_minus_1
    return f_minus_1


def fibonacci_2(n: int, cache={}) -> int:
    """
    Time complexity = O(n)
    Space complexity = O(n) due to caching.

    Test PASSED (46/46) [  <1 us]
    Average running time:   <1 us
    Median running time:    <1 us
    """
    if n <= 1:
        return n
    if n not in cache:
        cache[n] = fibonacci_2(n - 1) + fibonacci_2(n - 2)
    return cache[n]


def fibonacci_3(n: int, cache={}) -> int:
    """
    Time complexity = O(n)
    Space complexity = O(n) due to caching.

    Test PASSED (46/46) [  <1 us]
    Average running time:   <1 us
    Median running time:    <1 us
    """
    if n <= 1:
        return n
    if n not in cache:
        cache[n] = fibonacci_3(n - 1, cache) + fibonacci_3(n - 2, cache)
    return cache[n]


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('fibonacci.py', 'fibonacci.tsv',
                                       fibonacci_constant_space))
