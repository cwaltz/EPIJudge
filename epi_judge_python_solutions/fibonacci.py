import functools

from test_framework import generic_test


@functools.lru_cache(None)
# maxsize is set to None, the LRU feature is disabled & the cache can grow
# without bound.
def fibonacci(n: int) -> int:
    """
    Test PASSED (46/46) [  <1 us]
    Average running time:   <1 us
    Median running time:    <1 us
    """
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('fibonacci.py', 'fibonacci.tsv',
                                       fibonacci))
