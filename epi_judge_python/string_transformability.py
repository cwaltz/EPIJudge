import string
from collections import deque
from typing import NamedTuple

from test_framework import generic_test


class StringWithDistance(NamedTuple):
    candidate_string: str
    distance: int


def transform_string_optimized(dictionary: set[str], s: str, t: str) -> int:
    """
    Test PASSED (48/48) [ 387 us]
    Average running time:    1 ms
    Median running time:   386 us

    Finds the shortest transformation sequence from string `s` to `t`.
    Uses Bidirectional BFS for optimal performance.

    Args:
        dictionary: A set of valid strings for the transformation sequence.
        s: The starting string.
        t: The target string.

    Returns:
        The minimum number of steps to transform `s` into `t`, or -1 if
        impossible.
    """
    if s not in dictionary or t not in dictionary:
        return -1

    if s == t:
        return 0

    if len(s) != len(t):
        return -1

    # Local copy ensures thread-safety (no mutation of caller's data)
    word_set = dictionary.copy()  # Fastest method, explicitly designed for sets
    # word_set = set(dictionary)  # Marginally slower than .copy() but highly
    # readable.

    # Initialize bidirectional BFS frontiers
    begin_set = {s}
    end_set = {t}

    # Target is already in end_set and Source in begin_set,
    # so we remove them from word_set to avoid cycles
    word_set.discard(t)
    word_set.discard(s)

    distance = 0

    while begin_set and end_set:
        # Always expand the smaller frontier to minimize search space
        if len(begin_set) > len(end_set):
            begin_set, end_set = end_set, begin_set

        next_begin_set = set()

        for word in begin_set:
            # Generate all possible 1-character mutations
            for i in range(len(word)):
                for c in string.ascii_lowercase:
                    # Skip if the character is exactly the same
                    if c == word[i]:
                        continue

                    cand = word[:i] + c + word[i + 1:]

                    if cand in end_set:
                        # Intersection found! The two search trees have met.
                        return distance + 1

                    # Valid step forward
                    if cand in word_set:
                        next_begin_set.add(cand)
                        # Remove immediately to prevent other words in begin_set
                        # from queueing the same candidate (saves memory/time)
                        word_set.remove(cand)

        # Move to the next depth level
        begin_set = next_begin_set
        distance += 1

    # Frontiers did not intersect; no valid transformation sequence exists
    return -1


# Uses BFS to find the least steps of transformation.
def transform_string(dictionary: set[str], s: str, t: str) -> int:
    """
    #18.7

    Time complexity = O(d ** 2), where d is the number of words in dictionary.
    Space complexity = O(d)

    The number of vertices is d, the number of words in the dictionary. The
    number of edges is, in the worst-case, O(d ** 2). The time complexity is
    that of BFS, namely O(d + d ** 2) = O(d ** 2). If the string length n is
    less than d then the maximum number of edges out of a vertex is O(n),
    implying an O(n * d) bound.

    Test PASSED (48/48) [  97 us]
    Average running time:   49 ms
    Median running time:     9 ms
    """
    queue = deque([StringWithDistance(s, 0)])
    dictionary.remove(s)  # Marks s as visited by erasing it in D.

    while queue:
        f = queue.popleft()
        # Returns if we find a match.
        if f.candidate_string == t:
            return f.distance  # Number of steps reaches t.

        # Tries all possible transformations of f.candidate_string.
        for i in range(len(f.candidate_string)):
            for c in string.ascii_lowercase:  # Iterates through 'a' ~ 'z'.
                cand = f.candidate_string[:i] + c + f.candidate_string[i + 1:]
                if cand in dictionary:
                    dictionary.remove(cand)
                    queue.append(StringWithDistance(cand, f.distance + 1))

    return -1  # Cannot find a possible transformations.


def transform_string_pythonic(dictionary: set[str], s: str, t: str) -> int:
    """
    Time complexity = O(d ** 2), where d is the number of words in dictionary.
    Space complexity = O(d)

    Test PASSED (48/48) [  96 us]
    Average running time:   42 ms
    Median running time:     4 ms
    """
    if s == t:
        return 0
    length = 1
    running = {s}
    while running:
        running = dictionary & set(cand[:i] + c + cand[i + 1:]
                                   for cand in running
                                   for i in range(len(cand))
                                   for c in string.ascii_lowercase)
        if t in running:
            return length
        length += 1
        dictionary -= running
    return -1


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('string_transformability.py',
                                       'string_transformability.tsv',
                                       transform_string_optimized))
