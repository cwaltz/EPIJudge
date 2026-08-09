import collections
import functools
from typing import NamedTuple

from test_framework import generic_test
from test_framework.test_failure import TestFailure
from test_framework.test_utils import enable_executor_hook


# Subarray = collections.namedtuple('Subarray', ('start', 'end'))
class Subarray(NamedTuple):
    start: int
    end: int


def find_smallest_subarray_covering_set(
        paragraph: list[str], keywords: set[str]) -> Subarray:
    """
    #12.6

    Gemini refactored & improved the EPI version. Best for both - interviews
    and Enterprise Production

    Time complexity = O(n), n = len(paragraph) due to 'for' loop
        Yes, there is a 'while' loop inside the 'for' loop but left & right
        variables each increment by at most n over the course of execution.
    Space complexity = O(k), k = len(keywords) due to counter

    Test PASSED (904/904) [   3 us]
    Average running time:   21 us
    Median running time:     9 us
    """

    if not keywords or not paragraph:
        return Subarray(-1, -1)

    missing_words_counter = collections.Counter(keywords)
    # counter of missing keywords in the sliding window

    missing_words_total = len(keywords)
    # total number of missing keywords in the sliding window

    start, end = -1, -1  # Endpoints of the Subarray to be returned
    min_length = float('inf')  # Length of the Subarray to be returned
    left = 0  # Left endpoint of the sliding window: [left, right]

    for right, right_word in enumerate(paragraph):
        if right_word in keywords:
            missing_words_counter[right_word] -= 1
            if missing_words_counter[right_word] >= 0:
                # ... == 0: works as well where keywords is STRICTLY a set.
                # But we are using ... >= 0: to extend our solution to the
                # case where keywords is NOT a set and contains duplicates.
                # For example, keywords = ("apple", "apple", "banana")
                # Our initialization now would look like this:
                # missing_words_counter = {"apple": 2, "banana": 1}
                # missing_words_total = 3
                #
                # Our code would still work without any code changes. The >= 0
                # logic elegantly handles both unique words and duplicates.
                missing_words_total -= 1

        while missing_words_total == 0:
            current_length = right - left + 1

            if current_length < min_length:
                min_length = current_length
                start, end = left, right

            left_word = paragraph[left]
            if left_word in keywords:
                missing_words_counter[left_word] += 1
                if missing_words_counter[left_word] > 0:
                    missing_words_total += 1

            left += 1

    return Subarray(start, end)


def find_smallest_subarray_covering_set_epi(
        paragraph: list[str], keywords: set[str]) -> Subarray:
    """
    Test PASSED (904/904) [   4 us]
    Average running time:   42 us
    Median running time:    13 us
    """

    keywords_to_cover = collections.Counter(keywords)
    result = Subarray(start=-1, end=-1)
    remaining_to_cover = len(keywords)
    left = 0
    for right, p in enumerate(paragraph):
        if p in keywords:
            keywords_to_cover[p] -= 1
            if keywords_to_cover[p] >= 0:
                remaining_to_cover -= 1

        # Keeps advancing left until keywords_to_cover does not contain all
        # keywords.
        while remaining_to_cover == 0:
            if result == Subarray(
                    start=-1,
                    end=-1) or right - left < result.end - result.start:
                result = Subarray(start=left, end=right)
            pl = paragraph[left]
            if pl in keywords:
                keywords_to_cover[pl] += 1
                if keywords_to_cover[pl] > 0:
                    remaining_to_cover += 1
            left += 1
    return result


@enable_executor_hook
def find_smallest_subarray_covering_set_wrapper(executor, paragraph, keywords):
    copy = keywords

    (start, end) = executor.run(
        functools.partial(find_smallest_subarray_covering_set,
                          paragraph, keywords))

    if (start < 0 or start >= len(paragraph) or end < 0
            or end >= len(paragraph) or start > end):
        raise TestFailure('Index out of range')

    for i in range(start, end + 1):
        copy.discard(paragraph[i])

    if copy:
        raise TestFailure('Not all keywords are in the range')

    return end - start + 1


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main(
            'smallest_subarray_covering_set.py',
            'smallest_subarray_covering_set.tsv',
            find_smallest_subarray_covering_set_wrapper))
