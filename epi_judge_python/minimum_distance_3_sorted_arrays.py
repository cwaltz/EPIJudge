import typing
from typing import List

import bintrees
import sortedcontainers

from test_framework import generic_test


def find_closest_elements_in_sorted_arrays(
        sorted_arrays: List[List[int]]) -> int:
    """
    #14.6

    Time complexity = O(n log k), where n is the total number of elements in the
    k arrays.
    Space complexity = O(k) for the iters BST.

    Using sortedcontainers.

    For the special case k = 3 specified in the problem statement,
    the time complexity is O(n log 3) = O(n).

    Test PASSED (51/51) [  45 ms]
    Average running time:    1 ms
    Median running time:     1 ms
    """

    # Stores array iterators in each entry.
    iters = sortedcontainers.SortedDict()
    for idx, sorted_array in enumerate(sorted_arrays):
        it = iter(sorted_array)
        first_min = next(it, None)
        if first_min is not None:
            iters.setdefault((first_min, idx), it)

    min_distance_so_far = float('inf')
    while True:
        min_value, min_idx = iters.keys()[0]
        max_value = iters.keys()[-1][0]
        if max_value - min_value < min_distance_so_far:
            min_distance_so_far = max_value - min_value
        it = iters.pop(iters.keys()[0])
        next_min = next(it, None)
        # Return if some array has no remaining elements.
        if next_min is None:
            return typing.cast(int, min_distance_so_far)
        iters.setdefault((next_min, min_idx), it)


def find_closest_elements_in_sorted_arrays_using_bintrees(
        sorted_arrays: List[List[int]]) -> int:
    """
    Time complexity = O(n log k), where n is the total number of elements in
    the k arrays.
    Space complexity = O(k) for the iters BST.

    Using bintrees.

    For the special case k = 3 specified in the problem statement,
    the time complexity is O(n log 3) = O(n).

    Test PASSED (51/51) [ 125 ms]
    Average running time:    4 ms
    Median running time:     1 ms
    """

    # Stores array iterators in each entry.
    iters = bintrees.RBTree()
    for idx, sorted_array in enumerate(sorted_arrays):
        it = iter(sorted_array)
        first_min = next(it, None)
        if first_min is not None:
            iters.insert((first_min, idx), it)

    min_distance_so_far = float('inf')
    while True:
        min_value, min_idx = iters.min_key()
        max_value = iters.max_key()[0]
        if max_value - min_value < min_distance_so_far:
            min_distance_so_far = max_value - min_value
        it = iters.pop_min()[1]
        next_min = next(it, None)
        # Return if some array has no remaining elements.
        if next_min is None:
            return typing.cast(int, min_distance_so_far)
        iters.insert((next_min, min_idx), it)


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('minimum_distance_3_sorted_arrays.py',
                                       'minimum_distance_3_sorted_arrays.tsv',
                                       find_closest_elements_in_sorted_arrays))
