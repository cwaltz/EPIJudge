from test_framework import generic_test


# Module-level constants evaluated once at import time
_BRACKET_MAP = {')': '(', ']': '[', '}': '{'}
_OPENING_BRACKETS = set(_BRACKET_MAP.values())


def is_well_formed(s: str) -> bool:
    """
    #8.3

    Time complexity = O(n), where n = len(s)
    Space complexity = O(n), for stack

    Test PASSED (78/78) [  <1 us]
    Average running time:    8 us
    Median running time:    <1 us

    Evaluates whether a string of brackets is well-formed.

    A string is well-formed if every opening bracket is matched by a
    corresponding closing bracket in the correct order.

    Args:
        s (str): A string consisting entirely of '{', '}', '(', ')', '[', ']'.

    Returns:
        bool: True if the string is well-formed, False otherwise.

    Raises:
        ValueError: If the string contains characters outside the allowed
        bracket set.
    """
    if not s:
        return True

    # Quick optimization: an odd-length string cannot be perfectly paired
    if len(s) % 2 != 0:
        return False

    stack = []

    for c in s:
        if c in _OPENING_BRACKETS:
            stack.append(c)
        elif c in _BRACKET_MAP:
            if not stack or stack.pop() != _BRACKET_MAP[c]:
                return False
        else:
            raise ValueError(f"Invalid character encountered: '{c}'. "
                             f"Expected bracket characters only.")

    # If the stack is empty, all brackets were matched.
    return not stack


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('is_valid_parenthesization.py',
                                       'is_valid_parenthesization.tsv',
                                       is_well_formed))
