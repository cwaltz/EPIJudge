from typing import List, Tuple
import heapq

from test_framework import generic_test


# Pythonic solution, uses the heapq.merge() method which takes multiple inputs.
# def merge_sorted_arrays(sorted_arrays: List[List[int]]) -> List[int]:
def merge_sorted_arrays_pythonic(sorted_arrays):
    """
    Test PASSED (152/152) [  50 ms]
    Average running time:  554 us
    Median running time:   145 us
    """
    return list(heapq.merge(*sorted_arrays))


# def merge_sorted_arrays(sorted_arrays: List[List[int]]) -> List[int]:
def merge_sorted_arrays_1(sorted_arrays: List[List[int]]) -> List[int]:
    """
    #10.1

    Time complexity = O(n log k)
    Space complexity = O(k) beyond the space needed to write the final result.
    k is the number of input sequences
    n is the total number of trades

    Test PASSED (152/152) [  39 ms]
    Average running time:  587 us
    Median running time:   207 us
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


# def merge_sorted_arrays(sorted_arrays: List[List[int]]) -> List[int]:
def merge_sorted_arrays_2(sorted_arrays: List[List[int]]) -> List[int]:
    """
    Test PASSED (152/152) [  36 ms]
    Average running time:  627 us
    Median running time:   240 us
    """
    result: List[int] = []
    min_heap: List[Tuple[int, int, int]] = []
    # (value, index of the list, index of the value in the list)
    for index, sorted_array in enumerate(sorted_arrays):
        if sorted_array:
            heapq.heappush(min_heap, (sorted_array[0], index, 1))
    while min_heap:
        popped = heapq.heappop(min_heap)
        result.append(popped[0])
        list_index, index_in_list = popped[1], popped[2]
        if index_in_list < len(sorted_arrays[list_index]):
            heapq.heappush(min_heap, (sorted_arrays[list_index][index_in_list], list_index, index_in_list + 1))
    return result


# def merge_sorted_arrays(sorted_arrays: List[List[int]]) -> List[int]:
def merge_sorted_arrays_3(sorted_arrays: List[List[int]]) -> List[int]:
    """
    Test PASSED (152/152) [  39 ms]
    Average running time:  531 us
    Median running time:   177 us
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


def merge_sorted_arrays(sorted_arrays: List[List[int]]) -> List[int]:
# def merge_sorted_arrays_4(sorted_arrays: List[List[int]]) -> List[int]:
    """
    Test PASSED (152/152) [  33 ms]
    Average running time:  560 us
    Median running time:   214 us
    """
    # indices[i] gives us the index of the element in sorted_arrays[i] to be pushed next into heap
    indices = [1] * len(sorted_arrays)
    # min_heap stores tuples in the form (element, index of the array it belongs to)
    min_heap = [(sorted_array[0], i) for i, sorted_array in enumerate(sorted_arrays) if sorted_array]
    heapq.heapify(min_heap)

    result = []
    while min_heap:
        smallest = min_heap[0]
        result.append(smallest[0])
        index = smallest[1]
        if len(sorted_arrays[index]) > indices[index]:
            # sorted_arrays[index] array has unprocessed element(s).
            heapq.heappushpop(min_heap, (sorted_arrays[index][indices[index]], index))
            indices[index] += 1
        else:
            # No more elements are available in sorted_arrays[index] array.
            heapq.heappop(min_heap)
    return result


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('sorted_arrays_merge.py',
                                       'sorted_arrays_merge.tsv',
                                       merge_sorted_arrays))
