from typing import List

from test_framework import generic_test


def evaluate(expression: str) -> int:
    """
    Time complexity = O(n), where n is the length of the string. We perform O(1) computation per character of the
    string.
    Space complexity = O(n)

    Test PASSED (108/108) [   5 us]
    Average running time:  552 us
    Median running time:     2 us
    """
    intermediate_results: List[int] = []
    DELIMITER = ','
    OPERATORS = {
        '+': lambda y, x: x + y,
        '-': lambda y, x: x - y,
        '*': lambda y, x: x * y,
        '/': lambda y, x: x // y  # integer division
    }

    for token in expression.split(DELIMITER):
        if token in OPERATORS:
            intermediate_results.append(OPERATORS[token](
                intermediate_results.pop(), intermediate_results.pop()))
        else:  # token is a number
            intermediate_results.append(int(token))
    return intermediate_results[-1]


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('evaluate_rpn.py', 'evaluate_rpn.tsv',
                                       evaluate))
