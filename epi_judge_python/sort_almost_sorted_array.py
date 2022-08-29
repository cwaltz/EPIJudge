import heapq
import itertools
from typing import Iterator, List

from test_framework import generic_test


def sort_approximately_sorted_array(sequence: Iterator[int],
                                    k: int) -> List[int]:
    """
    #10.3

    Time complexity = O(n log k)
    Space complexity = O(k)

    Test PASSED (101/101) [   6 ms]
    Average running time:   75 us
    Median running time:     5 us
    """
    min_heap: List[int] = []
    # Adds the first k elements into min_heap. Stop if there are fewer than k elements.
    for x in itertools.islice(sequence, k):
        heapq.heappush(min_heap, x)

    result = []
    # For every new element, add it to min_heap and extract the smallest.
    for x in sequence:
        result.append(heapq.heappushpop(min_heap, x))

    # Extracts the remaining elements.
    result.extend(heapq.nsmallest(k, min_heap))

    return result


def sort_approximately_sorted_array_1(sequence: Iterator[int],
                                      k: int) -> List[int]:
    """
    Test PASSED (101/101) [   9 ms]
    Average running time:  102 us
    Median running time:     7 us
    """
    min_heap = []
    result = []
    for num in sequence:
        heapq.heappush(min_heap, num)
        if len(min_heap) == k + 1:
            smallest = heapq.heappop(min_heap)
            result.append(smallest)
    result.extend(heapq.nsmallest(k, min_heap))
    return result


def sort_approximately_sorted_array_wrapper(sequence, k):
    return sort_approximately_sorted_array(iter(sequence), k)


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main(
            'sort_almost_sorted_array.py', 'sort_almost_sorted_array.tsv',
            sort_approximately_sorted_array_wrapper))
