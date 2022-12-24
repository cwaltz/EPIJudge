from typing import List

from test_framework import generic_test


def matrix_in_spiral_order(matrix: List[List[int]]) -> List[int]:
    """
    #5.18

    Time complexity = O(r * c), r = # of rows, c = # of columns
    Space complexity = O(1)

    This solution works for non-square as well as square matrices. Easy to
    understand and implement.

    Effectively ~ 15 lines of code! :)

    Similar to Leetcode # 54. Spiral Matrix

    Source: Neetcode :)
    https://github.com/neetcode-gh/leetcode/blob/main/python/54-Spiral-Matrix.py

    Test PASSED (51/51) [ 214 us]
    Average running time:   78 us
    Median running time:    62 us
    """
    if not matrix:
        return []
    result = []
    top, bottom = 0, len(matrix)
    left, right = 0, len(matrix[0])

    while left < right and top < bottom:
        # Top row
        for col in range(left, right):
            result.append(matrix[top][col])
        top += 1

        # Right col
        for row in range(top, bottom):
            result.append(matrix[row][right - 1])
        right -= 1
        if left >= right or top >= bottom:
            break

        # Bottom row
        for col in range(right - 1, left - 1, -1):
            result.append(matrix[bottom - 1][col])
        bottom -= 1

        # Left col
        for row in range(bottom - 1, top - 1, -1):
            result.append(matrix[row][left])
        left += 1

    return result


def matrix_in_spiral_order_longer(matrix: List[List[int]]) -> List[int]:
    """
    #5.18

    Time complexity = O(r * c) where r and c are number of rows and columns.
    Space complexity = O(1)

    This solution works for non-square as well as square matrices. Easy to
    understand and implement.

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
    return (matrix and [*matrix.pop(0)] +
            matrix_in_spiral_order_pythonic([*zip(*matrix)][::-1]))


def square_matrix_in_spiral_order(square_matrix: List[List[int]]) -> List[int]:
    """
    Time complexity = O(n ^ 2) for an n x n square matrix.
    Space complexity = O(1)

    Test PASSED (51/51) [ 273 us]
    Average running time:  103 us
    Median running time:    75 us
    """
    size = len(square_matrix) - 1
    steps = len(square_matrix) // 2
    result = []
    for step in range(steps):
        for col in range(step, size - step):  # Top row from left to right
            result.append(square_matrix[step][col])
        for row in range(step, size - step):  # Right col from top to bottom
            result.append(square_matrix[row][size - 1 - step])
        for col in range(size - step, step, -1):  # Bottom row from right 2 left
            result.append(square_matrix[size - 1 - step][col])
        for row in range(size - step, step, -1):  # Left col from bottom to top
            result.append(square_matrix[row][step])

    if len(square_matrix) % 2 == 1:
        # Append the center element of the odd-sized matrix
        result.append(square_matrix[steps][steps])
    return result


def matrix_in_spiral_order_solution(square_matrix: List[List[int]]) -> List[int]:
    """
    Time complexity = O(n ** 2) where the size of the square matrix is n x n.

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
