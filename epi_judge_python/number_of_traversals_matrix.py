import itertools

from test_framework import generic_test


def number_of_ways(n: int, m: int) -> int:
    """
    #16.3

    Space efficient!

    Time complexity = O(n * m)
    Space complexity = O(min(n, m))

    Test PASSED (1775/1775) [  67 us]
    Average running time:   22 us
    Median running time:    21 us
    """
    if m == 1 or n == 1:
        return 1
    if n < m:
        n, m = m, n

    table = [1] * m
    for _ in range(1, n):
        for j in range(1, m):
            table[j] += table[j - 1]
    return table[-1]


# Pythonic implementation of space efficient solution.
def number_of_ways_pythonic(n: int, m: int) -> int:
    """
    Time complexity = O(n * m)
    Space complexity = O(min(n, m))

    Test PASSED (1775/1775) [  41 us]
    Average running time:   18 us
    Median running time:    16 us
    """
    if n < m:
        n, m = m, n

    table = [1] * m
    for _ in range(1, n):
        table = list(itertools.accumulate(table))
    return table[-1]


def number_of_ways_1(n: int, m: int) -> int:
    """
    Time complexity = O(n * m)
    Space complexity = O(n * m)

    Test PASSED (1775/1775) [  85 us]
    Average running time:   32 us
    Median running time:    29 us
    """
    if 1 in (m, n):
        return 1
    table = [[1] * n for _ in range(m)]
    for i in range(1, m):
        for j in range(1, n):
            table[i][j] = table[i - 1][j] + table[i][j - 1]
    return table[-1][-1]


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('number_of_traversals_matrix.py',
                                       'number_of_traversals_matrix.tsv',
                                       number_of_ways))
