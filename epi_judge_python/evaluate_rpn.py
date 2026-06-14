import operator

from test_framework import generic_test


def evaluate_rpn_using_operator_functions(exp: str) -> int:
    """
    #8.2

    Time complexity = O(n), where n is the length of the string.
        We perform O(1) computation per character of the string.
    Space complexity = O(n)

    Test PASSED (108/108) [   3 us]
    Average running time:  295 us
    Median running time:     1 us
    """
    # 1. Map operators directly to their functional equivalents
    OPERATIONS = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': lambda x, y: int(x / y)  # Truncates toward zero
    }

    stack = []

    # 2. Process tokens sequentially
    for token in exp.split(','):
        if token in OPERATIONS:
            # Explicitly pop right operand first to ensure strict math order
            right = stack.pop()
            left = stack.pop()
            stack.append(OPERATIONS[token](left, right))
        else:
            stack.append(int(token))

    return stack[0]


def evaluate_rpn_using_lambda_expressions(exp: str) -> int:
    """
    Test PASSED (108/108) [   3 us]
    Average running time:  307 us
    Median running time:     2 us
    """
    intermediate_results: list[int] = []
    DELIMITER = ','
    OPERATORS = {
        '+': lambda y, x: x + y,
        '-': lambda y, x: x - y,
        '*': lambda y, x: x * y,
        '/': lambda y, x: int(x / y)  # integer division
        # int(x / y) returns the integer closer to zero
        # int(5 / 2) = 2
        # int(-5 / 2) = -2
        # x // y returns the smaller integer
        # 5 // 2 = 2
        # -5 // 2 = -3
        # Hence, int(x / y) is NOT ALWAYS EQUAL to x // y
    }

    for token in exp.split(DELIMITER):
        if token in OPERATORS:
            intermediate_results.append(OPERATORS[token](
                intermediate_results.pop(), intermediate_results.pop()))
        else:  # token is a number
            intermediate_results.append(int(token))
    return intermediate_results[0]


def evaluate_rpn_using_match_case(exp: str) -> int:
    """
    Test PASSED (108/108) [   3 us]
    Average running time:  311 us
    Median running time:     1 us
    """
    tokens = exp.split(',')
    operators = '+-*/'
    stack = []

    for token in tokens:
        if token in operators:
            right = stack.pop()
            left = stack.pop()
            result = 0
            match token:
                case '+':
                    result = left + right
                case '-':
                    result = left - right
                case '*':
                    result = left * right
                case '/':
                    result = int(left / right)
            stack.append(result)
        else:
            stack.append(int(token))

    return stack[0]


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('evaluate_rpn.py', 'evaluate_rpn.tsv',
                                       evaluate_rpn_using_operator_functions))
