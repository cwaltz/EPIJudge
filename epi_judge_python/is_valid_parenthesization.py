from test_framework import generic_test


def is_well_formed(s: str) -> bool:
    """
    #8.3

    Time complexity = O(n), where n is the length of s
    Space complexity = O(n) for stack

    Test PASSED (78/78) [  <1 us]
    Average running time:    8 us
    Median running time:     1 us
    """
    if len(s) % 2 == 1:  # Odd length string can't be valid
        return False
    stack = []
    closing = {
        ')': '(',
        '}': '{',
        ']': '['
    }
    for c in s:
        if c not in closing:  # c is an opening bracket so push it on stack
            stack.append(c)
        elif not stack or stack.pop() != closing[c]:
            return False
    return not stack


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('is_valid_parenthesization.py',
                                       'is_valid_parenthesization.tsv',
                                       is_well_formed))
