from typing import List

from test_framework import generic_test


def plus_one(A: List[int]) -> List[int]:
    """
    #5.2

    Time complexity = O(n), where n is the length of A.
    Space complexity = O(1)

    Test PASSED (505/505) [   1 us]
    Average running time:    2 us
    Median running time:     2 us
    """
    if not A:
        return A
    A[-1] += 1
    for i in range(len(A) - 1, 0, -1):
        if A[i] != 10:
            break
        A[i] = 0
        A[i - 1] += 1
    if A[0] == 10:
        # There is a carry-out, so we need one more digit to store the result.
        # A slick way to do this is to append a 0 at the end of the array,
        # and update the first entry to 1.
        A[0] = 1
        A.append(0)
    return A


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('int_as_array_increment.py',
                                       'int_as_array_increment.tsv', plus_one))
