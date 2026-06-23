from collections import Counter
from collections.abc import Iterator

from test_framework import generic_test


def majority_search_constant_space(stream: Iterator[str]) -> str | None:
    """
    #17.5

    Boyer–Moore majority vote algorithm
    https://en.wikipedia.org/wiki/Boyer%E2%80%93Moore_majority_vote_algorithm

    Time complexity = O(n), where n is the number of elements in the input.
    Space complexity = O(1)

    Test PASSED (201/201) [   6 ms]
    Average running time:   43 us
    Median running time:     5 us
    """
    candidate, candidate_count = None, 0
    for it in stream:
        if candidate_count == 0:
            candidate = it
            candidate_count = 1
        elif candidate == it:
            candidate_count += 1
        else:  # candidate_count != 0 and candidate != it
            candidate_count -= 1
    return candidate


def majority_search_using_counter(stream: Iterator[str]) -> str | None:
    """
    Time complexity = O(n), where n is the number of elements in the input.
    Space complexity = O(n)

    Test PASSED (201/201) [   3 ms]
    Average running time:   36 us
    Median running time:     7 us
    """
    frequency = Counter(stream)
    result, max_count = None, 0
    for key, value in frequency.items():
        if max_count < value:
            max_count, result = value, key
    return result


def majority_search_using_counter_and_max(stream: Iterator[str]) -> str | None:
    """
    Time complexity = O(n), where n is the number of elements in the input.
    Space complexity = O(n)

    Test PASSED (201/201) [   3 ms]
    Average running time:   36 us
    Median running time:     8 us
    """
    frequency = Counter(stream)
    return max(frequency, key=frequency.get)


def majority_search_using_most_common(stream: Iterator[str]) -> str | None:
    """
    Time complexity = O(n), where n is the number of elements in the input.
    Space complexity = O(n)

    Test PASSED (201/201) [   3 ms]
    Average running time:   44 us
    Median running time:     8 us
    """
    return Counter(stream).most_common(1)[0][0]


def majority_search_wrapper(stream):
    return majority_search_constant_space(iter(stream))


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('majority_element.py',
                                       'majority_element.tsv',
                                       majority_search_wrapper))
