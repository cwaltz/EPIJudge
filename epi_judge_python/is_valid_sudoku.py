from test_framework import generic_test


def is_row_valid(partial_assignment: list[list[int]], row: int) -> bool:
    seen = set()
    for col in range(9):
        if partial_assignment[row][col]:
            if partial_assignment[row][col] in seen:
                return False
            else:
                seen.add(partial_assignment[row][col])
    return True


def is_col_valid(partial_assignment: list[list[int]], col: int) -> bool:
    seen = set()
    for row in range(9):
        if partial_assignment[row][col]:
            if partial_assignment[row][col] in seen:
                return False
            else:
                seen.add(partial_assignment[row][col])
    return True


def is_3x3_block_valid(
        partial_assignment: list[list[int]], row: int, col: int) -> bool:
    seen = set()
    for row_offset in range(3):
        for col_offset in range(3):
            if partial_assignment[row + row_offset][col + col_offset]:
                if (partial_assignment[row + row_offset][col + col_offset] in
                        seen):
                    return False
                else:
                    seen.add(partial_assignment[row + row_offset][col +
                                                                  col_offset])
    return True


def is_sudoku_valid_faster(partial_assignment: list[list[int]]) -> bool:
    """
    Test PASSED (745/745) [  30 us]
    Average running time:   20 us
    Median running time:    30 us
    """
    # Check rows
    for row in range(9):
        if not is_row_valid(partial_assignment, row):
            return False

    # Check cols
    for col in range(9):
        if not is_col_valid(partial_assignment, col):
            return False

    # Check 3x3 blocks
    for row in [0, 3, 6]:
        for col in [0, 3, 6]:
            if not is_3x3_block_valid(partial_assignment, row, col):
                return False

    return True


# Check if a partially filled matrix has any conflicts.
def is_valid_sudoku(partial_assignment: list[list[int]]) -> bool:
    """
    #5.17

    Time complexity = O(n ^ 2), for an n x n Sudoku grid.
    Space complexity = O(n), for the bit array used to check the constraints.
    n = 9 in this case.

    Test PASSED (745/745) [  39 us]
    Average running time:   26 us
    Median running time:    39 us
    """
    def validate_row(i: int) -> bool:
        seen = [False for _ in range(10)]
        for j in range(9):
            if partial_assignment[i][j] != 0:
                if seen[partial_assignment[i][j]]:
                    return False
                seen[partial_assignment[i][j]] = True
        return True

    def validate_col(j: int) -> bool:
        seen = [False for _ in range(10)]
        for i in range(9):
            if partial_assignment[i][j] != 0:
                if seen[partial_assignment[i][j]]:
                    return False
                seen[partial_assignment[i][j]] = True
        return True

    def validate_3x3_block(i: int, j: int) -> bool:
        seen = [False for _ in range(10)]
        for di in range(3):
            for dj in range(3):
                if partial_assignment[i + di][j + dj] != 0:
                    if seen[partial_assignment[i + di][j + dj]]:
                        return False
                    seen[partial_assignment[i + di][j + dj]] = True
        return True

    for row in range(9):
        if not validate_row(row):
            return False

    for col in range(9):
        if not validate_col(col):
            return False

    for row in [0, 3, 6]:
        for col in [0, 3, 6]:
            if not validate_3x3_block(row, col):
                return False

    return True


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('is_valid_sudoku.py',
                                       'is_valid_sudoku.tsv',
                                       is_sudoku_valid_faster))
