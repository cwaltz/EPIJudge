from typing import List, Tuple
import heapq

from test_framework import generic_test


def merge_sorted_arrays_0(sorted_arrays: List[List[int]]) -> List[int]:
    """
    #10.1

    Time complexity = O(n log k)
    Space complexity = O(k) beyond the space needed to write the final result.
    k is the number of input sequences
    n is the total number of trades

    Test PASSED (152/152) [  38 ms]
    Average running time:  565 us
    Median running time:   200 us
    """
    min_heap: List[Tuple[int, int]] = []
    # Builds a list of iterators for each array in sorted_arrays.
    sorted_arrays_iters = [iter(x) for x in sorted_arrays]

    # Puts first element from each iterator in min_heap.
    for i, it in enumerate(sorted_arrays_iters):
        first_element = next(it, None)
        if first_element is not None:
            heapq.heappush(min_heap, (first_element, i))

    result = []
    while min_heap:
        smallest_entry, smallest_array_i = heapq.heappop(min_heap)
        smallest_array_iter = sorted_arrays_iters[smallest_array_i]
        result.append(smallest_entry)
        next_element = next(smallest_array_iter, None)
        if next_element is not None:
            heapq.heappush(min_heap, (next_element, smallest_array_i))
    return result


def merge_sorted_arrays(sorted_arrays: List[List[int]]) -> List[int]:
    """
    Test PASSED (152/152) [  32 ms]
    Average running time:  563 us
    Median running time:   213 us
    """
    length = len(sorted_arrays)
    if length == 0:
        return []
    elif length == 1:
        return sorted_arrays[0]

    result = []
    min_heap = [(sorted_arrays[i][0], i, 1) for i in range(length)]
    heapq.heapify(min_heap)
    while min_heap:
        popped = heapq.heappop(min_heap)
        result.append(popped[0])
        if popped[2] < len(sorted_arrays[popped[1]]):
            heapq.heappush(min_heap, (sorted_arrays[popped[1]][popped[2]],
                                      popped[1], popped[2] + 1))

    return result


# Pythonic solution, uses the heapq.merge() method which takes multiple inputs.
def merge_sorted_arrays_pythonic(sorted_arrays: List[List[int]]) -> List[int]:
    """
    Test PASSED (152/152) [  50 ms]
    Average running time:  554 us
    Median running time:   145 us
    """
    return list(heapq.merge(*sorted_arrays))


def merge_sorted_arrays_2(sorted_arrays: List[List[int]]) -> List[int]:
    """
    Test PASSED (152/152) [  39 ms]
    Average running time:  516 us
    Median running time:   166 us
    """
    min_heap: List[Tuple[int, int]] = []
    # Builds a list of iterators for each array in sorted_arrays.
    sorted_arrays_iters = [iter(x) for x in sorted_arrays]

    # Puts first element from each iterator in min_heap.
    for i, it in enumerate(sorted_arrays_iters):
        first_element = next(it, None)
        if first_element is not None:
            heapq.heappush(min_heap, (first_element, i))

    result = []
    while min_heap:
        smallest_entry, smallest_array_i = min_heap[0]
        smallest_array_iter = sorted_arrays_iters[smallest_array_i]
        result.append(smallest_entry)
        next_element = next(smallest_array_iter, None)
        if next_element is None:
            # Nothing to push.
            heapq.heappop(min_heap)
        else:
            # Push the next element to min_heap.
            heapq.heappushpop(min_heap, (next_element, smallest_array_i))
    return result


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('sorted_arrays_merge.py',
                                       'sorted_arrays_merge.tsv',
                                       merge_sorted_arrays))
