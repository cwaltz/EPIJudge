from typing import List

from test_framework import generic_test


def fibonacci(n: int) -> int:
    if n < 2:
        return n
    fib: List[int] = [0] * (n + 1)
    fib[0], fib[1] = 0, 1
    for i in range(2, n + 1):
        fib[i] = fib[i - 1] + fib[i - 2]
    return fib[n]


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('fibonacci.py', 'fibonacci.tsv',
                                       fibonacci))
