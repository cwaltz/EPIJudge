import collections
from typing import Iterator

from test_framework import generic_test


def majority_search(stream: Iterator[str]) -> str:
    """
    #17.6

    Time complexity = O(n), where n is the number of elements in the input.
    Space complexity = O(1)

    Test PASSED (201/201) [   6 ms]
    Average running time:   45 us
    Median running time:     5 us
    """
    candidate, candidate_count = None, 0
    for it in stream:
        if candidate_count == 0:
            candidate = it
            candidate_count += 1
        elif candidate == it:
            candidate_count += 1
        else:  # candidate != it
            candidate_count -= 1
    return candidate


def majority_search_using_dict(stream: Iterator[str]) -> str:
    """
    Time complexity = O(n), where n is the number of elements in the input.
    Space complexity = O(n)

    Test PASSED (201/201) [   3 ms]
    Average running time:   39 us
    Median running time:     8 us
    """
    frequency: collections.Counter[str, int] = collections.Counter(stream)
    result, max_count = '', 0
    for key, value in frequency.items():
        if max_count < value:
            max_count, result = value, key
    return result


def majority_search_wrapper(stream):
    return majority_search(iter(stream))


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('majority_element.py',
                                       'majority_element.tsv',
                                       majority_search_wrapper))
