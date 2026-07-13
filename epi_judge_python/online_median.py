import heapq
from collections.abc import Iterator
from sortedcontainers import SortedList

from test_framework import generic_test


def online_median_fastest(sequence: Iterator) -> list[float]:
    """
    #10.5

    Time complexity = O(n log n)
    Space complexity = O(n), n = # of numbers consumed so far

    ~ 20 lines of code

    Test PASSED (55/55) [  23 ms]
    Average running time:  443 us
    Median running time:     6 us
    """
    min_heap, max_heap = [], []
    result = []

    for num in sequence:
        if not max_heap or num <= max_heap[0]:
            heapq.heappush_max(max_heap, num)
        else:  # elif num > max_heap[0]:
            heapq.heappush(min_heap, num)

        max_heap_size = len(max_heap)
        min_heap_size = len(min_heap)

        if abs(max_heap_size - min_heap_size) > 1:
            if max_heap_size > min_heap_size:
                heapq.heappush(min_heap, heapq.heappop_max(max_heap))
            else:  # elif max_heap_size < min_heap_size:
                heapq.heappush_max(max_heap, heapq.heappop(min_heap))
            result.append((max_heap[0] + min_heap[0]) / 2)
        elif max_heap_size == min_heap_size:
            result.append((max_heap[0] + min_heap[0]) / 2)
        elif max_heap_size > min_heap_size:
            result.append(max_heap[0])
        else:  # elif max_heap_size < min_heap_size:
            result.append(min_heap[0])

    return result


def online_median(sequence: Iterator[int]) -> list[float]:
    """
    < 10 lines of code

    This version is the most elegant because it leverages heappushpop to
    blindly balance the heaps without needing complex if/else checks on the
    incoming values.

    Time complexity = O(n log n)
    Space complexity = O(n), n = # of numbers consumed so far

    Test PASSED (55/55) [  45 ms]
    Average running time:  846 us
    Median running time:     8 us
    """
    # min_heap stores the larger half seen so far.
    min_heap: list[int] = []
    # max_heap stores the smaller half seen so far.
    # values in max_heap are negative
    max_heap: list[int] = []
    result = []

    for x in sequence:
        heapq.heappush_max(max_heap, heapq.heappushpop(min_heap, x))
        # Ensure min_heap and max_heap have equal number of elements if an even
        # number of elements is read; otherwise, min_heap must have one more
        # element than max_heap.
        if len(max_heap) > len(min_heap):
            heapq.heappush(min_heap, heapq.heappop_max(max_heap))

        result.append(0.5 * (min_heap[0] + (max_heap[0])) if len(min_heap) ==
                      len(max_heap) else min_heap[0])
    return result


def online_median_faster(sequence: Iterator[int]) -> list[float]:
    """
    Time complexity = O(n log n)
    Space complexity = O(n)

    Test PASSED (55/55) [  26 ms]
    Average running time:  500 us
    Median running time:     8 us
    """

    # min_heap stores the larger half seen so far.
    min_heap: list[int] = []
    # max_heap stores the smaller half seen so far.
    max_heap: list[int] = []
    result = []

    first_element = next(sequence, None)
    if first_element is not None:
        heapq.heappush(min_heap, first_element)
        result.append(first_element)

    for num in sequence:
        # Pushes incoming numbers into correct heap.
        if num < min_heap[0]:
            heapq.heappush_max(max_heap, num)
        else:
            heapq.heappush(min_heap, num)

        # Keeps the heaps of similar sizes (sizes can differ by at most 1).
        if abs(len(min_heap) - len(max_heap)) > 1:
            if len(max_heap) < len(min_heap):
                smallest = heapq.heappop(min_heap)
                heapq.heappush_max(max_heap, smallest)
            else:  # len(min_heap) < len(max_heap)
                greatest = heapq.heappop_max(max_heap)
                heapq.heappush(min_heap, greatest)

        # Appends the correct median value to the result list.
        if len(min_heap) == len(max_heap):
            result.append(0.5 * (min_heap[0] + max_heap[0]))
        elif len(max_heap) < len(min_heap):
            result.append(min_heap[0])
        else:  # len(min_heap) < len(max_heap)
            result.append(max_heap[0])
    return result


def online_median_using_sortedlist(sequence: Iterator[int]) -> list[float]:
    """
    Time complexity = O(n log n)
    Space complexity = O(n), n = # of numbers consumed so far

    Test PASSED (55/55) [ 179 ms]
    Average running time:    3 ms
    Median running time:    17 us
    """
    sortedlist = SortedList()
    result = []
    length = 0

    for num in sequence:
        length += 1
        sortedlist.add(num)
        if length % 2 == 0:
            result.append(
                (sortedlist[length // 2] + sortedlist[length // 2 - 1]) / 2)
        else:
            result.append(sortedlist[length // 2])

    return result


def online_median_wrapper(sequence):
    return online_median_using_sortedlist(iter(sequence))


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('online_median.py', 'online_median.tsv',
                                       online_median_wrapper))
