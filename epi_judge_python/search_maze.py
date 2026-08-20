import copy
import functools
from collections import deque
from typing import NamedTuple

from test_framework import generic_test
from test_framework.test_failure import TestFailure
from test_framework.test_utils import enable_executor_hook

WHITE, BLACK = range(2)
DIRECTIONS = [[0, 1], [0, -1], [1, 0], [-1, 0]]


class Coordinate(NamedTuple):
    x: int
    y: int


def _reconstruct_path(parent_map: dict[Coordinate, Coordinate | None],
                      end: Coordinate) -> list[Coordinate]:
    """Walks backward from the end node to start using the parent map."""
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = parent_map[current]
    path.reverse()
    return path


def search_maze_bfs(maze: list[list[int]], start: Coordinate,
                    end: Coordinate) -> list[Coordinate]:
    """
    Test PASSED (101/101) [   3 us]
    Average running time:   86 us
    Median running time:    35 us
    """
    if not maze or not maze[0]:
        return []

    rows, cols = len(maze), len(maze[0])

    def is_valid(x: int, y: int) -> bool:
        return 0 <= x < rows and 0 <= y < cols and maze[x][y] == WHITE

    if not is_valid(start.x, start.y) or not is_valid(end.x, end.y):
        return []

    # Map tracks `visited_node: node_we_came_from`
    # start maps to None since it's the origin.
    parent_map: dict[Coordinate, Coordinate | None] = {start: None}
    queue = deque([start])

    while queue:
        current = queue.popleft()

        if current == end:
            return _reconstruct_path(parent_map, end)

        for dx, dy in DIRECTIONS:
            neighbor = Coordinate(current.x + dx, current.y + dy)

            # If valid and not yet visited
            if is_valid(neighbor.x, neighbor.y) and neighbor not in parent_map:
                parent_map[neighbor] = current
                queue.append(neighbor)

    return []


def search_maze_dfs(maze: list[list[int]], start: Coordinate,
                    end: Coordinate) -> list[Coordinate]:
    """
    #18.1

    Test PASSED (101/101) [   2 us]
    Average running time:   81 us
    Median running time:    35 us
    """
    if not maze or not maze[0]:
        return []

    rows, cols = len(maze), len(maze[0])

    def is_valid(x: int, y: int) -> bool:
        return 0 <= x < rows and 0 <= y < cols and maze[x][y] == WHITE

    if not is_valid(start.x, start.y) or not is_valid(end.x, end.y):
        return []

    parent_map: dict[Coordinate, Coordinate | None] = {start: None}
    stack = [start]

    while stack:
        current = stack.pop()

        if current == end:
            return _reconstruct_path(parent_map, end)

        for dx, dy in DIRECTIONS:
            neighbor = Coordinate(current.x + dx, current.y + dy)

            if is_valid(neighbor.x, neighbor.y) and neighbor not in parent_map:
                parent_map[neighbor] = current
                stack.append(neighbor)

    return []


def search_maze(maze: list[list[int]], s: Coordinate,
                e: Coordinate) -> list[Coordinate]:
    """
    Time complexity = O(|V| + |E|)
    Space complexity = O(|V|)  # TODO: Is it correct?

    Test PASSED (101/101) [   2 us]
    Average running time:   53 us
    Median running time:    15 us
    """

    # Perform DFS to find a feasible path.
    def dfs(x: int, y: int) -> tuple[bool, list[Coordinate]]:
        if x == e.x and y == e.y:
            return True, [Coordinate(x, y)]

        # Checks (x, y) is within maze and is a white pixel.
        if not (0 <= x < rows and 0 <= y < cols) or maze[x][y] == BLACK:
            return False, []

        maze[x][y] = BLACK  # Mark it as visited.
        for i in range(4):
            path_exists, path = dfs(x + DIRECTIONS[i], y + DIRECTIONS[i + 1])
            if path_exists:
                return True, path + [Coordinate(x, y)]

        return False, []

    rows, cols = len(maze), len(maze[0])
    DIRECTIONS = [0, 1, 0, -1, 0]  # Right, Down, Left, Up in that order.
    path_exists, path = dfs(s.x, s.y)
    path.reverse()  # To start at s and finish at e.
    return path


def search_maze_epi_official(maze: list[list[int]], s: Coordinate,
                             e: Coordinate) -> list[Coordinate]:
    """
    Time complexity = O(|V| + |E|)
    Space complexity = O(|V|)  # TODO: Is it correct?

    Test PASSED (101/101) [   2 us]
    Average running time:   67 us
    Median running time:    31 us
    """

    # Perform DFS to find a feasible path.
    def search_maze_helper(cur: Coordinate):
        # Checks cur is within maze and is a white pixel.
        if not (0 <= cur.x < len(maze) and 0 <= cur.y < len(maze[cur.x])
                and maze[cur.x][cur.y] == WHITE):
            return False
        path.append(cur)
        maze[cur.x][cur.y] = BLACK
        if cur == e:
            return True

        if any(
                map(
                    search_maze_helper,
                    map(Coordinate, (cur.x - 1, cur.x + 1, cur.x, cur.x),
                        (cur.y, cur.y, cur.y - 1, cur.y + 1)))):
            return True
        # Cannot find a path, remove the entry added in path.append(cur).
        del path[-1]
        return False

    path: list[Coordinate] = []
    search_maze_helper(s)
    return path


def path_element_is_feasible(maze, prev, cur):
    if not ((0 <= cur.x < len(maze)) and
            (0 <= cur.y < len(maze[cur.x])) and maze[cur.x][cur.y] == WHITE):
        return False
    return cur == (prev.x + 1, prev.y) or \
        cur == (prev.x - 1, prev.y) or \
        cur == (prev.x, prev.y + 1) or \
        cur == (prev.x, prev.y - 1)


@enable_executor_hook
def search_maze_wrapper(executor, maze, s, e):
    s = Coordinate(*s)
    e = Coordinate(*e)
    cp = copy.deepcopy(maze)

    path = executor.run(functools.partial(search_maze_bfs, cp, s, e))

    if not path:
        return s == e

    if path[0] != s or path[-1] != e:
        raise TestFailure('Path doesn\'t lay between start and end points')

    for i in range(1, len(path)):
        if not path_element_is_feasible(maze, path[i - 1], path[i]):
            raise TestFailure('Path contains invalid segments')

    return True


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('search_maze.py', 'search_maze.tsv',
                                       search_maze_wrapper))
