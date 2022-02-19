import collections
from typing import List

from test_framework import generic_test
from test_framework.test_failure import TestFailure


class Stack:
    """
    The worst-case additional space complexity is O(n), which occurs when each key pushed is greater
    than all keys in the primary stack. However, when the number of distinct keys is small, or the
    maximum changes infrequently, the additional space complexity is less, O(1) in the best-case. The
    time complexity for each specified method is still O(1).
    """

    class MaxWithCount:
        def __init__(self, max: int, count: int) -> None:
            self.max = max
            self.count = count

    def __init__(self) -> None:
        self._elements: List[int] = []
        self._cached_max_with_count: List[Stack.MaxWithCount] = []

    def empty(self) -> bool:
        return len(self._elements) == 0

    def max(self) -> int:
        if self.empty():
            raise IndexError('max(): empty stack')
        return self._cached_max_with_count[-1].max

    def pop(self) -> int:
        if self.empty():
            raise IndexError('pop(): empty stack')
        popped = self._elements.pop()
        current_max = self._cached_max_with_count[-1].max
        if popped == current_max:
            self._cached_max_with_count[-1].count -= 1
            if self._cached_max_with_count[-1].count == 0:
                self._cached_max_with_count.pop()
        return popped

    def push(self, x: int) -> None:
        self._elements.append(x)
        if len(self._cached_max_with_count) == 0:
            self._cached_max_with_count.append(self.MaxWithCount(x, 1))
        else:
            current_max = self._cached_max_with_count[-1].max
            if x > current_max:
                self._cached_max_with_count.append(self.MaxWithCount(x, 1))
            elif x == current_max:
                self._cached_max_with_count[-1].count += 1


class StackV1:
    """
    Each of the specified methods has time complexity O(1).
    The additional space complexity is O(n), regardless of the stored keys.
    """

    ElementWithCachedMax = collections.namedtuple('ElementWithCachedMax',
                                                  ('element', 'max'))

    def __init__(self) -> None:

        self._elements: List[StackV1.ElementWithCachedMax] = []

    def empty(self) -> bool:

        return len(self._elements) == 0

    def max(self) -> int:

        if self.empty():
            raise IndexError('max(): stack is empty')
        return self._elements[-1].max

    def pop(self) -> int:

        if self.empty():
            raise IndexError('pop(): stack is empty')
        return self._elements.pop().element

    def push(self, x: int) -> None:

        self._elements.append(
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
