"""
An obvious extension (followup question) is if a valid path can be returned
instead of just a boolean value. The solutions for it have been added at the
end.
"""

import functools

from test_framework import generic_test

# Immutable tuple for thread safety
DIRECTIONS = ((0, 1), (0, -1), (1, 0), (-1, 0))


def is_pattern_contained_in_grid_interview(
        grid: list[list[int]], pattern: list[int]) -> bool:
    """
    #16.5

    Recursive DFS implementation

    Time complexity = O(r * c * n) in the worst case
        r = # of rows, c = # of columns in grid, n = len(pattern)
    Space complexity = O(r * c * n) due to caching

    Test PASSED (186/186) [  67 us]
    Average running time:  269 us
    Median running time:    24 us
    """
    if not pattern:
        return True

    if not grid or not grid[0]:
        return False

    # The following commented out pre-computation acts as a massive
    # short-circuit for impossible patterns. It somehow does not improve the
    # runtime here but should be used in a production setting.
    # grid_set = {num for row in grid for num in row}
    # pattern_set = set(pattern)
    # if not pattern_set.issubset(grid_set):
    #     return False

    rows, cols = len(grid), len(grid[0])

    @functools.lru_cache(None)
    def dfs(r: int, c: int, offset: int) -> bool:
        # Base case: We've matched every character in the pattern.
        # Return True to signify a successful end of the search.
        if offset == len(pattern):
            return True

        # Early return if out of bounds or the character does not match
        if (not (0 <= r < rows and 0 <= c < cols)
                or grid[r][c] != pattern[offset]):
            return False

        # Explore all 4 adjacent directions
        for dr, dc in DIRECTIONS:
            if dfs(r + dr, c + dc, offset + 1):
                return True

        # If all 4 directions fail, this path is a dead end
        return False

    # Try starting the DFS from every cell in the grid
    for row in range(rows):
        for col in range(cols):
            if dfs(row, col, offset=0):
                return True  # Return the first successful positive response

    return False


def is_pattern_contained_in_grid_prod(grid: list[list[int]],
                                      pattern: list[int]) -> bool:
    """
    Iterative BFS implementation

    Time complexity = O(r * c * n) in the worst case
        r = # of rows, c = # of columns in grid, n = len(pattern)
    Space complexity = O(r * c) due to queue

    Test PASSED (186/186) [  16 us]
    Average running time:   73 us
    Median running time:    12 us
    """
    if not pattern:
        return True  # An empty pattern is trivially found

    if not grid or not grid[0]:
        return False

    length = len(pattern)
    rows, cols = len(grid), len(grid[0])

    # Seed the initial valid set with coordinates matching the last character
    curr_set = {
        (row, col)
        for row in range(rows)
        for col in range(cols)
        if grid[row][col] == pattern[-1]
    }

    # Work backwards through the pattern
    for i in range(length - 2, -1, -1):
        # Short-circuit: If no valid paths remain, the pattern doesn't exist
        if not curr_set:
            return False

        next_set = set()
        for r, c in curr_set:
            for dr, dc in DIRECTIONS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == \
                        pattern[i]:
                    next_set.add((nr, nc))

        curr_set = next_set

    return bool(curr_set)


def is_pattern_contained_in_grid_epi(grid: list[list[int]],
                                     pattern: list[int]) -> bool:
    """
    Test PASSED (186/186) [  93 us]
    Average running time:  303 us
    Median running time:    35 us
    """

    @functools.lru_cache(None)
    def is_pattern_suffix_contained_starting_at_xy(x: int, y: int, offset: int):
        if len(pattern) == offset:
            # Nothing left to complete.
            return True

        # Early return if (x, y) lies outside the grid or the character
        # does not match, or we have already tried this combination.
        if (not (0 <= x < len(grid) and 0 <= y < len(grid[x]))
                or grid[x][y] != pattern[offset]):
            return False

        return any(
            is_pattern_suffix_contained_starting_at_xy(*next_xy, offset + 1)
            for next_xy in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)))

    return any(
        is_pattern_suffix_contained_starting_at_xy(i, j, offset=0)
        for i in range(len(grid)) for j in range(len(grid[i])))


# Extension


def find_pattern_path_recursive(
        grid: list[list[int]], pattern: list[int]) -> list[tuple[int, int]]:
    """
    Recursively finds a 1D pattern in a 2D grid and returns the sequence of
    (row, col) coordinates.
    Returns an empty list [] if the pattern is not found.
    """
    if not pattern:
        return []
    if not grid or not grid[0]:
        return []

    rows, cols = len(grid), len(grid[0])

    @functools.lru_cache(None)
    def dfs(r: int, c: int, offset: int) -> list[tuple[int, int]] | None:
        # Base case: We've matched every character in the pattern.
        # Return an empty list to signify a successful end of the path.
        if offset == len(pattern):
            return []

        # Early return if out of bounds or the character does not match
        if (not (0 <= r < rows and 0 <= c < cols) or
                grid[r][c] != pattern[offset]):
            return None

        # Explore all 4 adjacent directions
        for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            suffix_path = dfs(r + dr, c + dc, offset + 1)

            # If the recursive call didn't return None, it found a valid path
            if suffix_path is not None:
                # Prepend the current coordinate to the successful path
                return [(r, c)] + suffix_path

        # If all 4 directions fail, this path is a dead end
        return None

    # Try starting the DFS from every cell in the grid
    for row in range(rows):
        for col in range(cols):
            path = dfs(row, col, offset=0)
            if path is not None:
                return path  # Return the first successful path we find

    return []


def find_pattern_path_iterative(
        grid: list[list[int]], pattern: list[int]) -> list[tuple[int, int]]:
    """
    Finds a 1D pattern in a 2D grid and returns the sequence of (row, col)
    coordinates.
    Returns an empty list [] if the pattern is not found.
    """
    length = len(pattern)
    if length == 0:
        return []

    rows = len(grid)
    if rows == 0:
        return []

    cols = len(grid[0])
    if cols == 0:
        return []

    # Map current coordinate -> list of coordinates representing the path to
    # the end
    # Seed it with the last character of the pattern
    curr_paths = {
        (r, c): [(r, c)]
        for r in range(rows)
        for c in range(cols)
        if grid[r][c] == pattern[-1]
    }

    # Work backward from the second-to-last character to the first
    for i in range(length - 2, -1, -1):
        if not curr_paths:
            return []  # Short-circuit if no valid paths remain

        next_paths = {}
        for (r, c), path_to_end in curr_paths.items():
            for dr, dc in DIRECTIONS:
                nr, nc = r + dr, c + dc

                # Check bounds and character match
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == \
                        pattern[i]:
                    # If multiple paths converge on the same cell, we only need
                    # to keep one.
                    # This prevents exponential branching.
                    if (nr, nc) not in next_paths:
                        next_paths[(nr, nc)] = [(nr, nc)] + path_to_end

        curr_paths = next_paths

    # If the loop finishes and curr_paths is not empty, we found at least one
    # full path.
    # Return any of the valid paths (e.g., the first one we pull from the
    # dictionary).
    if curr_paths:
        return next(iter(curr_paths.values()))

    return []


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('is_string_in_matrix.py',
                                       'is_string_in_matrix.tsv',
                                       is_pattern_contained_in_grid_interview))
