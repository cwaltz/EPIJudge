import collections

from test_framework import generic_test

WHITE, BLACK, TOUCHING = 'W', 'B', 'T'
DIRECTIONS = ((0, 1), (0, -1), (1, 0), (-1, 0))


def fill_surrounded_regions(board: list[list[str]]) -> None:
    """
    #18.3

    Iterative BFS version recommended for both - interviews and production

    Time complexity = O(r * c), r = len(board), c = len(board[0])
    Space complexity = O(r * c), a loose upper bound for queue

    Test PASSED (51/51) [   9 ms]
    Average running time:  387 us
    Median running time:   106 us
    """
    if not board or not board[0]:
        return

    rows, cols = len(board), len(board[0])
    queue = collections.deque()

    # OPTIMIZATION: Only add boundary elements if they are WHITE
    # Check first and last rows
    for c in range(cols):
        if board[0][c] == WHITE:
            queue.append((0, c))
        if board[rows - 1][c] == WHITE:
            queue.append((rows - 1, c))

    # Check first and last columns (avoiding double-counting the corners)
    for r in range(1, rows - 1):
        if board[r][0] == WHITE:
            queue.append((r, 0))
        if board[r][cols - 1] == WHITE:
            queue.append((r, cols - 1))

    # BFS to mark all boundary-connected WHITEs as TOUCHING
    while queue:
        r, c = queue.popleft()
        if board[r][c] == WHITE:
            board[r][c] = TOUCHING
            # Look at neighbors
            for dr, dc in DIRECTIONS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == WHITE:
                    queue.append((nr, nc))

    # Final pass: TOUCHING back to WHITE, completely surrounded WHITE to BLACK
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == TOUCHING:
                board[r][c] = WHITE
            elif board[r][c] == WHITE:
                board[r][c] = BLACK


def fill_surrounded_regions_recursive(board: list[list[str]]) -> None:
    """
    Test PASSED (51/51) [  11 ms]
    Average running time:  493 us
    Median running time:   140 us
    """
    if not board or not board[0]:
        return

    rows, cols = len(board), len(board[0])
    if rows < 3 or cols < 3:
        return

    touching_regions = set()  # NOT surrounded regions

    def dfs(r: int, c: int) -> None:
        if (not (0 <= r < rows) or not (0 <= c < cols) or
                board[r][c] == BLACK or (r, c) in touching_regions):
            return

        touching_regions.add((r, c))
        for dr, dc in DIRECTIONS:
            dfs(r + dr, c + dc)

    for col in range(cols):
        dfs(0, col)
        dfs(rows - 1, col)

    for row in range(1, rows - 1):
        dfs(row, 0)
        dfs(row, cols - 1)

    for row in range(1, rows - 1):
        for col in range(1, cols - 1):
            if board[row][col] == WHITE and (row, col) not in touching_regions:
                board[row][col] = BLACK


def fill_surrounded_regions_epi(board: list[list[str]]) -> None:
    """
    Test PASSED (51/51) [   4 ms]
    Average running time:  314 us
    Median running time:   130 us
    """
    rows, cols = len(board), len(board[0])
    queue = collections.deque([(i, j) for k in range(rows)
                               for i, j in ((k, 0), (k, cols - 1))] +
                              [(i, j) for k in range(cols)
                               for i, j in ((0, k), (rows - 1, k))])

    while queue:
        x, y = queue.popleft()
        if 0 <= x < rows and 0 <= y < cols and board[x][y] == 'W':
            board[x][y] = 'T'
            queue.extend([(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)])

    board[:] = [['B' if c != 'T' else 'W' for c in row] for row in board]


def fill_surrounded_regions_wrapper(board):
    fill_surrounded_regions(board)
    return board


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('matrix_enclosed_regions.py',
                                       'matrix_enclosed_regions.tsv',
                                       fill_surrounded_regions_wrapper))
