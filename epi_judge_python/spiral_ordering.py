from typing import List

from test_framework import generic_test


def matrix_in_spiral_order(square_matrix: List[List[int]]) -> List[int]:
    """
    #5.18
    The time complexity is O(n ^ 2) where the size of the square matrix is n x n.
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
