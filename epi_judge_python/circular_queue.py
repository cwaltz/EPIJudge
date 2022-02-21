from test_framework import generic_test
from test_framework.test_failure import TestFailure


class Queue:

    SCALE_FACTOR = 2

    def __init__(self, capacity: int) -> None:

        self._data = [None] * capacity
        self._head = self._tail = self._num_of_entries = 0

    def enqueue(self, x: int) -> None:

        if self._num_of_entries == len(self._data):
            # Need to resize. Make the queue elements appear consecutively.
            self._data = self._data[self._head:] + self._data[:self._head]
            # Reset head and tail.
            self._head, self._tail = 0, self._num_of_entries
            self._data += [None] * (len(self._data) * (self.SCALE_FACTOR - 1))

        self._data[self._tail] = x
        self._tail = (self._tail + 1) % len(self._data)
        self._num_of_entries += 1

    def dequeue(self) -> int:

        if self._num_of_entries == 0:
            raise IndexError('dequeue() on an empty queue')
        result = self._data[self._head]
        self._head = (self._head + 1) % len(self._data)
        self._num_of_entries -= 1
        return result

    def size(self) -> int:

        return self._num_of_entries


def queue_tester(ops):
    q = Queue(1)

    for (op, arg) in ops:
        if op == 'Queue':
            q = Queue(arg)
        elif op == 'enqueue':
            q.enqueue(arg)
        elif op == 'dequeue':
            result = q.dequeue()
            if result != arg:
                raise TestFailure('Dequeue: expected ' + str(arg) + ', got ' +
                                  str(result))
        elif op == 'size':
            result = q.size()
            if result != arg:
                raise TestFailure('Size: expected ' + str(arg) + ', got ' +
                                  str(result))
        else:
            raise RuntimeError('Unsupported queue operation: ' + op)


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('circular_queue.py',
                                       'circular_queue.tsv', queue_tester))
