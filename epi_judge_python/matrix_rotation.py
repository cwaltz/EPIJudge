from typing import List

from test_framework import generic_test


def rotate_matrix(square_matrix: List[List[int]]) -> None:
    """
    #5.19

    Time complexity = O(n * n), where n = len(square_matrix)
    Space complexity = O(1)

    Same as Leetcode # 48. Rotate Image

    Only 4 lines of code! :)

    Take following values to come up with the assignment inside for loops:
    n = 5, i = 0, j = 1

    Test PASSED (51/51) [ 245 us]
    Average running time:   83 us
    Median running time:    61 us
    """
    matrix_size = len(square_matrix) - 1
    for i in range(len(square_matrix) // 2):
        for j in range(i, matrix_size - i):
            # Perform a 4-way exchange. Note that A[~i] for i in [0, len(A) - 1]
            # is A[-(i + 1)].
            (square_matrix[i][j], square_matrix[~j][i], square_matrix[~i][~j],
             square_matrix[j][~i]) = (square_matrix[~j][i],
                                      square_matrix[~i][~j],
                                      square_matrix[j][~i],
                                      square_matrix[i][j])


def rotate_matrix_pythonic(matrix: List[List[int]]) -> None:
    """
    Test PASSED (51/51) [  24 us]
    Average running time:   10 us
    Median running time:     8 us
    """
    # matrix[::-1] flips the matrix upside down
    # zip() transposes it
    matrix[:] = map(list, zip(*matrix[:: -1]))


def rotate_matrix_using_list_comprehension(matrix: List[List[int]]) -> None:
    """
    Test PASSED (51/51) [ 102 us]
    Average running time:   38 us
    Median running time:    30 us
    """
    # matrix[::-1] flips the matrix upside down
    matrix[:] = [[row[i] for row in matrix[:: -1]] for i in range(len(matrix))]


def rotate_matrix_wrapper(square_matrix):
    rotate_matrix(square_matrix)
    return square_matrix


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('matrix_rotation.py',
                                       'matrix_rotation.tsv',
                                       rotate_matrix_wrapper))
