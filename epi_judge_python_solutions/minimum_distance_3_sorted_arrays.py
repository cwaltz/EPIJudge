import typing
from typing import List

import bintrees

from test_framework import generic_test


def find_closest_elements_in_sorted_arrays(sorted_arrays: List[List[int]]
                                           ) -> int:
    """
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
