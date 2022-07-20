from typing import List

from test_framework import generic_test


def matrix_in_spiral_order(matrix: List[List[int]]) -> List[int]:
    """
    #5.18

    Time complexity = O(r * c) where r and c are number of rows and columns.
    Space complexity = O(1)

    This solution works for non-square as well as square matrices. Easy to understand and implement.

    Test PASSED (51/51) [ 237 us]
    Average running time:   87 us
    Median running time:    67 us
    """
    last_row = len(matrix) - 1
    if last_row == -1:
        return []
    if last_row == 0:
        return matrix[0]
    last_col = len(matrix[0]) - 1
    if last_col == 0:
        return [matrix[row][0] for row in range(last_row + 1)]

    result = []
    first_row, first_col = 0, 0

    while True:
        if last_col < first_col:
            break
        for col in range(first_col, last_col + 1):
            result.append(matrix[first_row][col])
        first_row += 1

        if last_row < first_row:
            break
        for row in range(first_row, last_row + 1):
            result.append(matrix[row][last_col])
        last_col -= 1

        if last_col < first_col:
            break
        for col in range(last_col, first_col - 1, -1):
            result.append(matrix[last_row][col])
        last_row -= 1

        if last_row < first_row:
            break
        for row in range(last_row, first_row - 1, -1):
            result.append(matrix[row][first_col])
        first_col += 1

    return result


def matrix_in_spiral_order_pythonic(matrix: List[List[int]]) -> List[int]:
    """
    https://leetcode.com/problems/spiral-matrix/discuss/20571/1-liner-in-Python-%2B-Ruby

    Test PASSED (51/51) [   1 ms]
    Average running time:  390 us
    Median running time:   162 us
    """
    return matrix and [*matrix.pop(0)] + matrix_in_spiral_order_pythonic([*zip(*matrix)][::-1])


def square_matrix_in_spiral_order(square_matrix: List[List[int]]) -> List[int]:
    """
    Time complexity = O(n ^ 2) for an n x n square matrix.
    Space complexity = O(1)

    Test PASSED (51/51) [ 273 us]
    Average running time:  103 us
    Median running time:    75 us
    """
    size = len(square_matrix)
    steps = size // 2
    result = []
    for step in range(steps):
        for col in range(step, size - 1 - step):  # Top row from left to right.
            result.append(square_matrix[step][col])
        for row in range(step, size - 1 - step):  # Right column from top to bottom.
            result.append(square_matrix[row][size - 1 - step])
        for col in range(size - 1 - step, step, -1):  # Bottom row from right to left.
            result.append(square_matrix[size - 1 - step][col])
        for row in range(size - 1 - step, step, -1):  # Left column from bottom to top.
            result.append(square_matrix[row][step])

    if size % 2 == 1:  # Append the center element of the odd-sized matrix.
        result.append(square_matrix[steps][steps])
    return result


def matrix_in_spiral_order_solution(square_matrix: List[List[int]]) -> List[int]:
    """
    The time complexity is O(n ^ 2) where the size of the square matrix is n x n.

    Test PASSED (51/51) [ 964 us]
    Average running time:  266 us
    Median running time:   143 us
    """
    def matrix_layer_in_clockwise(offset: int):
        # handle odd length case
        if offset == len(square_matrix) - offset - 1:
            # square_matrix has odd dimension, and we are at the center of the
            # matrix square_matrix.
            # 1 -> 0, 3 -> 1, 5 -> 2
            result.append(square_matrix[offset][offset])
            return

        result.extend(square_matrix[offset][offset:-1 - offset])
        result.extend(list(zip(*square_matrix))[-1 - offset][offset:-1 - offset])
        result.extend(square_matrix[-1 - offset][-1 - offset:offset:-1])
        result.extend(list(zip(*square_matrix))[offset][-1 - offset:offset:-1])

    result: List[int] = []
    for offset in range((len(square_matrix) + 1) // 2):
        # 1, 2 -> [0] -> range(1)
        # 3, 4 -> [0, 1] -> range(2)
        # 5, 6 -> [0, 1, 2] -> range(3)
        matrix_layer_in_clockwise(offset)
    return result


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('spiral_ordering.py',
                                       'spiral_ordering.tsv',
                                       matrix_in_spiral_order))
