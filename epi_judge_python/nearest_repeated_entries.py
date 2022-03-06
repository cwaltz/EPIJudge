import typing
from typing import Dict, List

from test_framework import generic_test


def find_nearest_repetition(paragraph: List[str]) -> int:

    last_index_of_word: Dict[str, int] = {}
    minimum_distance = float('inf')
    for index, word in enumerate(paragraph):
        if word in last_index_of_word:
            minimum_distance = min(minimum_distance, index - last_index_of_word[word])
        last_index_of_word[word] = index
    return typing.cast(int, minimum_distance) if minimum_distance != float('inf') else -1


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('nearest_repeated_entries.py',
                                       'nearest_repeated_entries.tsv',
                                       find_nearest_repetition))
