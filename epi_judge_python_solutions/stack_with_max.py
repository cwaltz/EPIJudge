import collections
from typing import List

from test_framework import generic_test
from test_framework.test_failure import TestFailure


class Stack:
    """
    Each of the specified methods has time complexity O(1).
    The additional space complexity is O(n), regardless of the stored keys.

    Test PASSED (101/101) [   9 ms]
    Average running time:  128 us
    Median running time:    14 us
    """
    ElementWithCachedMax = collections.namedtuple('ElementWithCachedMax',
                                                  ('element', 'max'))

    def __init__(self) -> None:
        self._element_with_cached_max: List[Stack.ElementWithCachedMax] = []

    def empty(self) -> bool:

        return len(self._element_with_cached_max) == 0

    def max(self) -> int:

        return self._element_with_cached_max[-1].max

    def pop(self) -> int:

        return self._element_with_cached_max.pop().element

    def push(self, x: int) -> None:

        self._element_with_cached_max.append(
            self.ElementWithCachedMax(
                x, x if self.empty() else max(x, self.max())))


def stack_tester(ops):
    try:
        s = Stack()

        for (op, arg) in ops:
            if op == 'Stack':
                s = Stack()
            elif op == 'push':
                s.push(arg)
            elif op == 'pop':
                result = s.pop()
                if result != arg:
                    raise TestFailure('Pop: expected ' + str(arg) + ', got ' +
                                      str(result))
            elif op == 'max':
                result = s.max()
                if result != arg:
                    raise TestFailure('Max: expected ' + str(arg) + ', got ' +
                                      str(result))
            elif op == 'empty':
                result = int(s.empty())
                if result != arg:
                    raise TestFailure('Empty: expected ' + str(arg) +
                                      ', got ' + str(result))
            else:
                raise RuntimeError('Unsupported stack operation: ' + op)
    except IndexError:
        raise TestFailure('Unexpected IndexError exception')


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('stack_with_max.py',
                                       'stack_with_max.tsv', stack_tester))
