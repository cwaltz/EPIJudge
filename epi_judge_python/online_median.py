import heapq
from typing import Iterator, List

from test_framework import generic_test


def online_median(sequence: Iterator[int]) -> List[float]:
    """
    Time complexity  = O(n log n)
    Space complexity = O(n)

    Test PASSED (55/55) [  41 ms]
    Average running time:  792 us
    Median running time:    13 us
    """

    # min_heap stores the larger half seen so far.
    min_heap: List[int] = []
    # max_heap stores the smaller half seen so far.
    # values in max_heap are negative.
    max_heap: List[int] = []
    result = []

    first_element = next(sequence, None)
    if first_element is not None:
        heapq.heappush(min_heap, first_element)
        result.append(first_element)

    for num in sequence:
        # Pushes incoming numbers into correct heap.
        if num < min_heap[0]:
            heapq.heappush(max_heap, -num)
        else:
            heapq.heappush(min_heap, num)

        # Keeps the heaps of similar sizes (sizes can differ by at most 1).
        if abs(len(min_heap) - len(max_heap)) > 1:
            if len(max_heap) < len(min_heap):
                smallest = heapq.heappop(min_heap)
                heapq.heappush(max_heap, -smallest)
            else:  # len(min_heap) < len(max_heap)
                greatest = -heapq.heappop(max_heap)
                heapq.heappush(min_heap, greatest)

        # Appends the correct median value to the result list.
        if len(min_heap) == len(max_heap):
            result.append(0.5 * (min_heap[0] + (-max_heap[0])))
        elif len(max_heap) < len(min_heap):
            result.append(min_heap[0])
        else:  # len(min_heap) < len(max_heap)
            result.append(-max_heap[0])
    return result


def online_median_wrapper(sequence):
    return online_median(iter(sequence))


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('online_median.py', 'online_median.tsv',
                                       online_median_wrapper))
