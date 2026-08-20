from collections import deque

from test_framework import generic_test

DIRECTIONS = [[0, 1], [0, -1], [1, 0], [-1, 0]]


def flip_color_iterative_bfs(x: int, y: int, image: list[list[bool]]) -> None:
    """
    Time complexity = O(m * n), m = # of rows, n = # of cols.
    Space complexity = O(m + n)

    The time complexity is the same as that of BFS, i.e., O(mn). The space
    complexity is a little better than the worst-case for BFS, since there are
    at most O(m + n) vertices that are at the same distance from a given entry.

    Test PASSED (50/50) [   2 us]
    Average running time:   16 us
    Median running time:     7 us
    """
    if not image or not image[0]:
        return

    rows, cols = len(image), len(image[0])
    if not (0 <= x < rows and 0 <= y < cols):
        return

    color = image[x][y]
    image[x][y] = not color
    queue = deque([(x, y)])

    while queue:
        old_x, old_y = queue.popleft()
        for dx, dy in DIRECTIONS:
            next_x, next_y = old_x + dx, old_y + dy
            if (0 <= next_x < rows and 0 <= next_y < cols and
                    image[next_x][next_y] == color):
                image[next_x][next_y] = not color
                queue.append((next_x, next_y))


def flip_color_iterative_dfs(x: int, y: int, image: list[list[bool]]) -> None:
    """
    #18.2

    Test PASSED (50/50) [   2 us]
    Average running time:   16 us
    Median running time:     7 us
    """
    if not image or not image[0]:
        return

    rows, cols = len(image), len(image[0])
    if not (0 <= x < rows and 0 <= y < cols):
        return

    # Iterative DFS
    color = image[x][y]
    image[x][y] = not color
    stack = [(x, y)]

    while stack:
        old_x, old_y = stack.pop()
        for dx, dy in DIRECTIONS:
            next_x, next_y = old_x + dx, old_y + dy
            if (0 <= next_x < rows and 0 <= next_y < cols and
                    image[next_x][next_y] == color):
                image[next_x][next_y] = not color
                stack.append((next_x, next_y))


def flip_color_recursive_dfs(x: int, y: int, image: list[list[bool]]) -> None:
    """
    Test PASSED (50/50) [   2 us]
    Average running time:   16 us
    Median running time:     7 us
    """
    if not image or not image[0]:
        return

    rows, cols = len(image), len(image[0])
    if not (0 <= x < rows and 0 <= y < cols):
        return

    color = image[x][y]

    def flip_color_helper(i: int, j: int) -> None:
        for di, dj in DIRECTIONS:
            next_i, next_j = i + di, j + dj
            if (0 <= next_i < rows and 0 <= next_j < cols and
                    image[next_i][next_j] == color):
                image[next_i][next_j] = not color
                flip_color_helper(next_i, next_j)

    image[x][y] = not color
    flip_color_helper(x, y)


def flip_color_wrapper(x, y, image):
    flip_color_iterative_bfs(x, y, image)
    return image


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('matrix_connected_regions.py',
                                       'painting.tsv', flip_color_wrapper))
