import collections


class QueueWithMax:
    """
    Time complexity = O(1), for enqueue and dequeue are the same as that of the library queue.
    Time complexity = O(n), for finding the maximum. n is the number of entries.
    """
    def __init__(self) -> None:
        self._data = collections.deque()

    def enqueue(self, x: int) -> None:
        self._data.append(x)

    def dequeue(self) -> int:
        return self._data.popleft()

    def max(self) -> int:
        return max(self._data)
