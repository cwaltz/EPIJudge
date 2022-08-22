import functools
from typing import List

from test_framework import generic_test
from test_framework.test_utils import enable_executor_hook


# Assume s is a list of strings, each of which is of length 1, e.g.,
# ['r', 'a', 'm', ' ', 'i', 's', ' ', 'c', 'o', 's', 't', 'l', 'y'].
def reverse_words(s: List[str]):
    """
    Test PASSED (103/103) [  54 ms]
    Average running time:  530 us
    Median running time:     2 us
    """
    # First, reverse the whole string.
    s.reverse()

    def reverse_range(s, start, end):
        while start < end:
            s[start], s[end] = s[end], s[start]
            start, end = start + 1, end - 1

    start = 0
    while True:
        try:
            end = s.index(' ', start)
        except ValueError:  # Search key not found.
            break
        # Reverses each word in the string.
        reverse_range(s, start, end - 1)
        start = end + 1
    # Reverses the last word.
    reverse_range(s, start, len(s) - 1)


# Assume s is a list of strings, each of which is of length 1, e.g.,
# ['r', 'a', 'm', ' ', 'i', 's', ' ', 'c', 'o', 's', 't', 'l', 'y'].
def reverse_words_1(s: List[str]):
    """
    #6.5

    Time complexity = O(n), where n is the length of the string.
    Space complexity = O(1)

    Test PASSED (103/103) [ 115 ms]
    Average running time:    1 ms
    Median running time:     4 us
    """
    def reverse_word(start: int, end: int) -> None:
        while start < end:
            s[start], s[end] = s[end], s[start]
            start += 1
            end -= 1

    s.reverse()
    start, end = 0, 0
    while end < len(s):
        while end < len(s) and s[end] != ' ':
            end += 1
        reverse_word(start, end - 1)
        end += 1
        start = end


@enable_executor_hook
def reverse_words_wrapper(executor, s):
    s_copy = list(s)

    executor.run(functools.partial(reverse_words, s_copy))

    return ''.join(s_copy)


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('reverse_words.py', 'reverse_words.tsv',
                                       reverse_words_wrapper))
