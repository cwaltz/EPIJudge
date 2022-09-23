import functools

from test_framework import generic_test


def levenshtein_distance(a: str, b: str) -> int:
    """
    #16.2

    Time complexity = O(len_a * len_b)
    Space complexity = O(min(len_a, len_b))

    Test PASSED (100/100) [   1 ms]
    Average running time:  614 us
    Median running time:   321 us
    """
    # Let b be the smaller string of the two input strings.
    if len(a) < len(b):
        a, b = b, a
    len_a, len_b = len(a), len(b)
    # Initialize a distance matrix with 2 rows and len_b cols.
    d = [[-1] * len_b for _ in range(2)]
    # Initialize the 1st cell of the 1st row.
    d[0][0] = 0 if a[0] == b[0] else 1
    # Initialize the 1st row.
    for j in range(1, len_b):
        d[0][j] = j if a[0] == b[j] else 1 + d[0][j - 1]
    for i in range(1, len_a):
        # Initialize the 1st cell of the 2nd (new) row.
        d[1][0] = i if a[i] == b[0] else 1 + d[0][0]
        for j in range(1, len_b):
            d[1][j] = d[0][j - 1] if a[i] == b[j] else 1 + min(
                d[0][j - 1], d[0][j], d[1][j - 1])
        # Copy the 2nd row to the 1st row for the next iteration.
        d[0] = d[1][:]
    return d[0][-1]


def levenshtein_distance_1(a: str, b: str) -> int:
    """
    Time complexity = O(len_a * len_b)
    Space complexity = O(len_a * len_b)

    Test PASSED (100/100) [   2 ms]
    Average running time:  656 us
    Median running time:   340 us
    """
    len_a, len_b = len(a), len(b)
    # Initialize a distance matrix with len_a rows and len_b cols.
    d = [[-1] * len_b for _ in a]
    # Initialize the 1st cell of the 1st row.
    d[0][0] = 0 if a[0] == b[0] else 1
    # Initialize the 1st row.
    for j in range(1, len_b):
        d[0][j] = j if a[0] == b[j] else 1 + d[0][j - 1]
    # Initialize the 1st column.
    for i in range(1, len_a):
        d[i][0] = i if a[i] == b[0] else 1 + d[i - 1][0]
    for i in range(1, len_a):
        for j in range(1, len_b):
            d[i][j] = d[i - 1][j - 1] if a[i] == b[j] else 1 + min(
                d[i - 1][j - 1], d[i - 1][j], d[i][j - 1])
    return d[-1][-1]


def levenshtein_distance_using_cache(A: str, B: str) -> int:
    """
    Time complexity = O(len_a * len_b)
    Space complexity = O(len_a * len_b)

    Test PASSED (100/100) [   3 ms]
    Average running time:  979 us
    Median running time:   463 us
    """

    @functools.lru_cache(None)
    def compute_distance_between_prefixes(A_idx, B_idx):
        if A_idx < 0:
            # A is empty so add all of B's characters.
            return B_idx + 1
        elif B_idx < 0:
            # B is empty so delete all of A's characters.
            return A_idx + 1

        if A[A_idx] == B[B_idx]:
            return compute_distance_between_prefixes(A_idx - 1, B_idx - 1)

        substitute_last = compute_distance_between_prefixes(A_idx - 1,
                                                            B_idx - 1)
        add_last = compute_distance_between_prefixes(A_idx, B_idx - 1)
        delete_last = compute_distance_between_prefixes(A_idx - 1, B_idx)
        return 1 + min(substitute_last, add_last, delete_last)

    return compute_distance_between_prefixes(len(A) - 1, len(B) - 1)


def levenshtein_distance_2(a: str, b: str) -> int:
    """
    Time complexity = O(len_a * len_b)
    Space complexity = O(len_a * len_b)

    Test PASSED (100/100) [   3 ms]
    Average running time:    1 ms
    Median running time:   381 us
    """

    def compute_distance_between_prefixes(a_idx, b_idx):
        if a_idx < 0:
            # A is empty so add all of B's characters.
            return b_idx + 1
        elif b_idx < 0:
            # B is empty so delete all of A's characters.
            return a_idx + 1
        if distance_between_prefixes[a_idx][b_idx] == -1:
            if a[a_idx] == b[b_idx]:
                distance_between_prefixes[a_idx][b_idx] = (
                    compute_distance_between_prefixes(a_idx - 1, b_idx - 1))
            else:
                substitute_last = compute_distance_between_prefixes(a_idx - 1,
                                                                    b_idx - 1)
                add_last = compute_distance_between_prefixes(a_idx - 1, b_idx)
                delete_last = compute_distance_between_prefixes(a_idx,
                                                                b_idx - 1)
                distance_between_prefixes[a_idx][b_idx] = (
                        1 + min(substitute_last, add_last, delete_last))
        return distance_between_prefixes[a_idx][b_idx]

    distance_between_prefixes = [[-1] * len(b) for _ in a]
    return compute_distance_between_prefixes(len(a) - 1, len(b) - 1)


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('levenshtein_distance.py',
                                       'levenshtein_distance.tsv',
                                       levenshtein_distance))
