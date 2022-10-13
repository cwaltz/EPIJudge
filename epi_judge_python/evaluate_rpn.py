from math import ceil, floor
from typing import List

from test_framework import generic_test


def evaluate(expression: str) -> int:
    """
    #8.2

    Time complexity = O(n), where n is the length of the string. We perform O(1)
    computation per character of the string.
    Space complexity = O(n)

    Test PASSED (108/108) [   5 us]
    Average running time:  550 us
    Median running time:     2 us
    """
    intermediate_results: List[int] = []
    DELIMITER = ','
    OPERATORS = {
        '+': lambda y, x: x + y,
        '-': lambda y, x: x - y,
        '*': lambda y, x: x * y,
        '/': lambda y, x: x // y  # integer division
        # int(x / y) returns the integer closer to zero
        # int(5 / 2) = 2
        # int(-5 / 2) = -2
        # x // y returns the smaller integer
        # 5 // 2 = 2
        # -5 // 2 = -3
        # Hence, int(x / y) is NOT ALWAYS EQUAL to x // y
    }

    for token in expression.split(DELIMITER):
        if token in OPERATORS:
            intermediate_results.append(OPERATORS[token](
                intermediate_results.pop(), intermediate_results.pop()))
        else:  # token is a number
            intermediate_results.append(int(token))
    return intermediate_results[0]


def evaluateFaster(expression: str) -> int:
    """
    Test PASSED (108/108) [   4 us]
    Average running time:  506 us
    Median running time:     2 us
    """
    stack = []
    operators = "+-*/"
    DELIMITER = ','
    for token in expression.split(DELIMITER):
        if token not in operators:
            stack.append(int(token))
        else:
            if token == '+':
                stack.append(stack.pop() + stack.pop())
            elif token == '-':
                stack.append(-stack.pop() + stack.pop())
            elif token == '*':
                stack.append(stack.pop() * stack.pop())
            else:  # token = '/'
                divisor = stack.pop()
                t = (stack.pop() / divisor)
                stack.append(floor(t) if t > 0 else ceil(t))
    return stack[0]


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('evaluate_rpn.py', 'evaluate_rpn.tsv',
                                       evaluate))
