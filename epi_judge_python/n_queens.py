from test_framework import generic_test


def n_queens(n: int) -> list[list[int]]:
    """
    Test PASSED (10/10) [  77 ms]
    Average running time:    9 ms
    Median running time:   143 us
    """
    if n == 1:
        return [[0]]
    if n < 4:
        return []

    def n_queens_helper(cols: list[int], sums_set: set[int],
                        diffs_set: set[int]) -> None:
        for i in range(n):
            if i in cols:
                # There is a queen in the same column
                continue

            cols_length = len(cols)

            if cols_length + i in sums_set:
                # There is a queen in the same trailing diagonal
                continue
            local_sums_set = sums_set.copy()
            local_sums_set.add(cols_length + i)

            if cols_length - i in diffs_set:
                # There is a queen in the same leading diagonal
                continue
            local_diffs_set = diffs_set.copy()
            local_diffs_set.add(cols_length - i)

            local_cols = cols[:]
            local_cols.append(i)
            if len(local_cols) == n:
                result.append(local_cols[:])
            else:
                n_queens_helper(local_cols, local_sums_set, local_diffs_set)

    result = []
    n_queens_helper([], set(), set())
    return result


def n_queens_0(n: int) -> list[list[int]]:
    """
    #15.2

    Time complexity = O(n! / (c ** n)), where n is the number of queens.
    Space complexity = ?  # TODO

    The time complexity is lower bounded by the number of non-attacking
    placements.
    No exact form is known for this quantity as a function of n,
    but it is conjectured to tend to n! / (c ** n), where c ~ 2.54, which is
    super-exponential.

    Test PASSED (10/10) [ 356 ms]
    Average running time:   44 ms
    Median running time:   454 us
    """
    def solve_n_queens(row):
        if row == n:
            # All queens are legally placed.
            result.append(col_placement.copy())
            return
        for col in range(n):
            # Test if a newly placed queen will conflict any earlier queens
            # placed before.
            if all(
                    abs(c - col) not in (0, row - i)
                    for i, c in enumerate(col_placement[:row])):
                col_placement[row] = col
                solve_n_queens(row + 1)

    result: list[list[int]] = []
    col_placement = [0] * n
    solve_n_queens(0)
    return result


def comp(a, b):
    return sorted(a) == sorted(b)


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('n_queens.py', 'n_queens.tsv', n_queens,
                                       comp))
