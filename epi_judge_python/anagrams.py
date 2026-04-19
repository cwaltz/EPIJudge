import collections

from test_framework import generic_test, test_utils


def find_anagrams(dictionary: list[str]) -> list[list[str]]:
    """
    #12.0(b)
    Similar to Leetcode # 49. Group Anagrams

    Time complexity = O(nm log m), n = len(dictionary)
    Space complexity = O(nm), m = max([len(s) for s in dictionary])

    The computation consists of n calls to sort & n insertions into the hash
    table. Sorting all the keys has time complexity O(nm log m). The
    insertions add a time complexity of O(nm), yielding O(nm log m) time
    complexity in total.

    Test PASSED (9/9) [  46 ms]
    Average running time:   17 ms
    Median running time:     9 ms
    """
    sorted_string_to_anagrams: collections.defaultdict[
        str, list[str]] = collections.defaultdict(list)
    for s in dictionary:
        # Sorts the string, uses it as a key, and then appends the original
        # string as another value into hash table.
        sorted_string_to_anagrams[''.join(sorted(s))].append(s)
    return [
        group for group in sorted_string_to_anagrams.values()
        if len(group) >= 2
    ]


def find_anagrams_1(dictionary: list[str]) -> list[list[str]]:
    """
    Test PASSED (9/9) [  45 ms]
    Average running time:   16 ms
    Median running time:     9 ms
    """
    sorted_string_to_anagrams: collections.defaultdict[
        tuple, list[str]] = collections.defaultdict(list)
    for s in dictionary:
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
