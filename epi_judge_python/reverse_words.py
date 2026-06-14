import functools

from test_framework import generic_test
from test_framework.test_utils import enable_executor_hook


def reverse_range(s: list[str], start: int, end: int) -> None:
    while start < end:
        s[start], s[end] = s[end], s[start]
        start, end = start + 1, end - 1


# Assume s is a list of strings, each of which is of length 1, e.g.,
# ['r', 'a', 'm', ' ', 'i', 's', ' ', 'c', 'o', 's', 't', 'l', 'y'].
def reverse_words_using_library_index_method(s: list[str]) -> None:
    """
    #6.6

    Time complexity = O(n), where n is the length of the string.
    Space complexity = O(1)

    Test PASSED (103/103) [  43 ms]
    Average running time:  421 us
    Median running time:     1 us
    """
    # First, reverse the whole string.
    s.reverse()

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


def reverse_words_without_index_method(s: list[str]):
    """
    Test PASSED (103/103) [  88 ms]
    Average running time:  861 us
    Median running time:     2 us
    """
    def reverse_word(left: int, right: int) -> None:
        while left < right:
            s[left], s[right] = s[right], s[left]
            left += 1
            right -= 1

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

    executor.run(functools.partial(reverse_words_using_library_index_method,
                                   s_copy))

    return ''.join(s_copy)


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('reverse_words.py',
                                       'reverse_words.tsv',
                                       reverse_words_wrapper))
