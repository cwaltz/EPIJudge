import collections
from typing import List

from test_framework import generic_test


def flip_color(x: int, y: int, image: List[List[bool]]) -> None:
    """
    #18.2

    DFS (recursive)

    Time complexity = O(m * n), m = # of rows, n = # of cols.
    Space complexity = O(m * n) on the function call stack.

    The time complexity is the same as that of DFS, i.e., O(mn).

    Test PASSED (50/50) [   3 us]
    Average running time:   27 us
    Median running time:    12 us
    """
    color = image[x][y]
    image[x][y] = 1 - image[x][y]  # Flips.
    for d in (0, 1), (0, -1), (1, 0), (-1, 0):
        next_x, next_y = x + d[0], y + d[1]
        if (0 <= next_x < len(image) and 0 <= next_y < len(image[next_x])
                and image[next_x][next_y] == color):
            flip_color(next_x, next_y, image)


def flip_color_bfs(x: int, y: int, image: List[List[bool]]) -> None:
    """
    BFS (iterative)

    Time complexity = O(m * n), m = # of rows, n = # of cols.
    Space complexity = O(m + n)

    The time complexity is the same as that of BFS, i.e., O(mn). The space
    complexity is a little better than the worst-case for BFS, since there are
    at most O(m + n) vertices that are at the same distance from a given entry.

    Test PASSED (50/50) [   3 us]
    Average running time:   25 us
    Median running time:    11 us
    """
    color = image[x][y]
    q = collections.deque([(x, y)])
    image[x][y] = not image[x][y]  # Flips.
    while q:
        x, y = q.popleft()
        for next_x, next_y in ((x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)):
            if (0 <= next_x < len(image) and 0 <= next_y < len(image[next_x])
                    and image[next_x][next_y] == color):
                # Flips the color.
                image[next_x][next_y] = not image[next_x][next_y]
                q.append((next_x, next_y))


def flip_color_wrapper(x, y, image):
    flip_color(x, y, image)
    return image


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('matrix_connected_regions.py',
                                       'painting.tsv', flip_color_wrapper))
