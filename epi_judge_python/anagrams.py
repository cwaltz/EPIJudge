import collections
from typing import DefaultDict, List

from test_framework import generic_test, test_utils


def find_anagrams(dictionary: List[str]) -> List[List[str]]:
    """
    #12.0

    Time complexity = O(nm log m), where n is the number of strings and m is the maximum string length.
    Space complexity = O(nm)

    The computation consists of n calls to sort and n insertions into the hash table. Sorting all the keys has time
    complexity O(nm log m). The insertions add a time complexity of O(nm), yielding O(nm log m) time complexity in
    total.

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


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main(
            'anagrams.py',
            'anagrams.tsv',
            find_anagrams,
            comparator=test_utils.unordered_compare))
