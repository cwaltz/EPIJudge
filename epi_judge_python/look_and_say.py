import itertools

from test_framework import generic_test


def next_number(s: str) -> str:
    """Generates the next sequence in the look-and-say pattern."""
    length = len(s)
    i = 0
    result_as_list = []

    while i < length:
        count = 1
        while i + 1 < length and s[i + 1] == s[i]:
            count += 1
            i += 1

        result_as_list.append(str(count))
        result_as_list.append(s[i])
        i += 1

    return ''.join(result_as_list)


def look_and_say_interview(n: int) -> str:
    """
    #6.8

    Returns the nth integer in the look-and-say sequence as a string.

    The precise time complexity is a function of the lengths of the terms,
    which is extremely hard to analyze. Each successive number can have at most
    twice as many digits as the previous number - this happens when all digits
    are different. This means the maximum length number has length no more than
    2 ** n. Since there are n iterations and the work in each iteration is
    proportional to the length of the number computed in the iteration,
    a simple bound on the time complexity is O(n * (2 ** n)).

    Time complexity = O(n * (2 ** n))
    Space complexity = O(n * (2 ** n))

    Test PASSED (40/40) [  44 ms]
    Average running time:    4 ms
    Median running time:   221 us
    """
    if n <= 0:
        raise ValueError("n must be a positive integer greater than 0.")

    result = '1'
    for _ in range(n - 1):
        result = next_number(result)

    return result


def look_and_say_epi(n: int) -> str:
    """
    Test PASSED (40/40) [  53 ms]
    Average running time:    5 ms
    Median running time:   255 us
    """
    def next_number_inner(s: str):
        result_as_list, i = [], 0
        while i < len(s):
            count = 1
            while i + 1 < len(s) and s[i] == s[i + 1]:
                i += 1
                count += 1
            result_as_list.append(str(count) + s[i])
            i += 1
        return ''.join(result_as_list)

    result = '1'
    for _ in range(n - 1):
        result = next_number_inner(result)
    return result


# Pythonic solution uses the power of itertools.groupby().
def look_and_say_pythonic(n: int) -> str:
    """
    Test PASSED (40/40) [  55 ms]
    Average running time:    5 ms
    Median running time:   319 us
    """
    s = '1'
    for _ in range(n - 1):
        s = ''.join(
            str(len(list(group))) + key
            for key, group
            in itertools.groupby(s))
    return s


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main(
            'look_and_say.py',
            'look_and_say.tsv',
            look_and_say_interview))
