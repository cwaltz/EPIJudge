import collections
from typing import DefaultDict, List

from test_framework import generic_test, test_utils


def find_anagrams(dictionary: List[str]) -> List[List[str]]:
    """
    #12.0(a)
    Similar to Leetcode # 49. Group Anagrams

    Time complexity = O(nm log m), n = len(dictionary)
    Space complexity = O(nm), m = max([len(s) for s in dictionary])

    The computation consists of n calls to sort & n insertions into the hash
    table. Sorting all the keys has time complexity O(nm log m). The
    insertions add a time complexity of O(nm), yielding O(nm log m) time
    complexity in total.

    Test PASSED (9/9) [  51 ms]
    Average running time:   19 ms
    Median running time:    10 ms
    """
    sorted_string_to_anagrams: DefaultDict[
        str, List[str]] = collections.defaultdict(list)
    for s in dictionary:
        # Sorts the string, uses it as a key, and then appends the original
        # string as another value into hash table.
        sorted_string_to_anagrams[''.join(sorted(s))].append(s)
    return [
        group for group in sorted_string_to_anagrams.values()
        if len(group) >= 2
    ]


def find_anagrams_slower(dictionary: List[str]) -> List[List[str]]:
    """
    #12.0(a)
    Similar to Leetcode # 49. Group Anagrams

    Time complexity = O(nm log m), n = len(dictionary)
    Space complexity = O(nm), m = max([len(s) for s in dictionary])

    The computation consists of n calls to sort & n insertions into the hash
    table. Sorting all the keys has time complexity O(nm log m). The
    insertions add a time complexity of O(nm), yielding O(nm log m) time
    complexity in total.

    Test PASSED (9/9) [  58 ms]
    Average running time:   21 ms
    Median running time:    11 ms
    """
    sorted_string_to_anagrams: DefaultDict[
        tuple, List[str]] = collections.defaultdict(list)
    for s in dictionary:
        # Sorts the string, uses it as a key, and then appends the original
        # string as another value into hash table.
        sorted_string_to_anagrams[tuple(sorted(s))].append(s)
    return [
        group for group in sorted_string_to_anagrams.values()
        if len(group) >= 2
    ]


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main(
            'anagrams.py',
            'anagrams.tsv',
            find_anagrams,
            comparator=test_utils.unordered_compare))
