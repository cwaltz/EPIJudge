from typing import cast

from test_framework import generic_test


def find_nearest_repetition(paragraph: list[str]) -> int:
    """
    #12.5

    Time complexity = O(n), where n is the array length.
    Space complexity = O(d), where d is the number of distinct entries in the
        array.

    Test PASSED (505/505) [   5 us]
    Average running time:   17 us
    Median running time:     9 us
    """
    last_index_of_word: dict[str, int] = {}
    minimum_distance = float('inf')
    for index, word in enumerate(paragraph):
        if word in last_index_of_word:
            if index - last_index_of_word[word] < minimum_distance:
                minimum_distance = index - last_index_of_word[word]
        last_index_of_word[word] = index
    return cast(int, minimum_distance) if minimum_distance != float('inf') \
        else -1


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('nearest_repeated_entries.py',
                                       'nearest_repeated_entries.tsv',
                                       find_nearest_repetition))
