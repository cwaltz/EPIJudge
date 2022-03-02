import heapq
import itertools
from typing import Iterator, List

from test_framework import generic_test


def sort_approximately_sorted_array(sequence: Iterator[int],
                                    k: int) -> List[int]:
    """
    Test PASSED (101/101) [   6 ms]
    Average running time:   76 us
    Median running time:     8 us
    """
    min_heap: List[int] = []
    for num in itertools.islice(sequence, k):
        heapq.heappush(min_heap, num)

    result: List[int] = []
    for num in sequence:
        smallest = heapq.heappushpop(min_heap, num)
        result.append(smallest)

    result.extend(heapq.nsmallest(k, min_heap))
    return result


def sort_approximately_sorted_array_v1(sequence: Iterator[int],
                                       k: int) -> List[int]:
    """
    Test PASSED (101/101) [   9 ms]
    Average running time:  108 us
    Median running time:     9 us
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
