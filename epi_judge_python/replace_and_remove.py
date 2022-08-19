import functools
from typing import List

from test_framework import generic_test
from test_framework.test_utils import enable_executor_hook


def replace_and_remove(size: int, s: List[str]) -> int:
    """
    #6.4

    Time complexity = O(n), where n is the length of the string.
    Space complexity = O(1)

    Test PASSED (501/501) [  13 ms]
    Average running time:   35 us
    Median running time:     4 us
    """
    # Forward iteration: remove 'b's and count the number of 'a's.
    a_count, write_index = 0, 0
    for i in range(size):
        if s[i] != 'b':
            s[write_index] = s[i]
            write_index += 1
            if s[i] == 'a':
                a_count += 1

    # Backward iteration: replace 'a's with 'dd's starting from the end.
    new_size = write_index + a_count
    read_index = write_index - 1
    write_index = new_size - 1

    while read_index >= 0:
        if s[read_index] == 'a':
            s[write_index - 1:write_index + 1] = 'dd'
            write_index -= 2
        else:
            s[write_index] = s[read_index]
            write_index -= 1
        read_index -= 1

    return new_size


@enable_executor_hook
def replace_and_remove_wrapper(executor, size, s):
    res_size = executor.run(functools.partial(replace_and_remove, size, s))
    return s[:res_size]


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('replace_and_remove.py',
                                       'replace_and_remove.tsv',
                                       replace_and_remove_wrapper))
