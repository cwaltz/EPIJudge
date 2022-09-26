import collections
import string
from typing import Set

from test_framework import generic_test

# Uses BFS to find the least steps of transformation.


def transform_string(D: Set[str], s: str, t: str) -> int:
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
    StringWithDistance = collections.namedtuple(
        'StringWithDistance', ('candidate_string', 'distance'))
    q = collections.deque([StringWithDistance(s, 0)])
    D.remove(s)  # Marks s as visited by erasing it in D.

    while q:
        f = q.popleft()
        # Returns if we find a match.
        if f.candidate_string == t:
            return f.distance  # Number of steps reaches t.

        # Tries all possible transformations of f.candidate_string.
        for i in range(len(f.candidate_string)):
            for c in string.ascii_lowercase:  # Iterates through 'a' ~ 'z'.
                cand = f.candidate_string[:i] + c + f.candidate_string[i + 1:]
                if cand in D:
                    D.remove(cand)
                    q.append(StringWithDistance(cand, f.distance + 1))
    return -1  # Cannot find a possible transformations.


def transform_string_pythonic(D: Set[str], s: str, t: str) -> int:
    """
    Time complexity = O(d ** 2), where d is the number of words in dictionary.
    Space complexity = O(d)

    Test PASSED (48/48) [ 102 us]
    Average running time:   43 ms
    Median running time:     4 ms
    """
    if s == t:
        return 0
    length = 1
    running = {s}
    while running:
        running = D & set(cand[:i] + c + cand[i + 1:] for cand in running
                          for i in range(len(cand))
                          for c in string.ascii_lowercase)
        if t in running:
            return length
        length += 1
        D -= running
    return -1


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('string_transformability.py',
                                       'string_transformability.tsv',
                                       transform_string))
