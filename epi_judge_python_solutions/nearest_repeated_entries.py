import typing
from typing import Dict, List

from test_framework import generic_test


def find_nearest_repetition(paragraph: List[str]) -> int:
    """
    The time complexity is O(n), since we perform a constant amount of work per entry.
    The space complexity is O(d), where d is the number of distinct entries in the array.
    """

    word_to_latest_index: Dict[str, int] = {}
    nearest_repeated_distance = float('inf')
    for i, word in enumerate(paragraph):
        if word in word_to_latest_index:
            latest_equal_word = word_to_latest_index[word]
            nearest_repeated_distance = min(nearest_repeated_distance,
                                            i - latest_equal_word)
        word_to_latest_index[word] = i
    return typing.cast(int, nearest_repeated_distance
                       ) if nearest_repeated_distance != float('inf') else -1


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('nearest_repeated_entries.py',
                                       'nearest_repeated_entries.tsv',
                                       find_nearest_repetition))
