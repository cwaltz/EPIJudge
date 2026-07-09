"""
#19.0 Parallel Computing

Parallel computing boot camp

A semaphore is a very powerful synchronization construct. Conceptually, a
semaphore maintains a set of permits. A thread calling acquire() on a semaphore
waits, if necessary, until a permit is available, and then takes it. A thread
calling release() on a semaphore adds a permit and notifies threads waiting on
that semaphore, potentially releasing a blocking acquirer.
"""

import threading
from types import TracebackType
from typing import Type


class Semaphore:
    """A modernized, robust Semaphore implementation."""

    def __init__(self, max_available: int):
        if max_available < 0:
            raise ValueError(
                "Semaphore cannot be initialized with a negative value.")

        self._condition = threading.Condition()
        self._max_available = max_available
        self._taken = 0

    def acquire(self) -> None:
        # Industry standard: ALWAYS use context managers for locks
        with self._condition:
            while self._taken == self._max_available:
                self._condition.wait()
            self._taken += 1

    def release(self) -> None:
        with self._condition:
            if self._taken == 0:
                raise ValueError("Semaphore released too many times.")
            self._taken -= 1
            self._condition.notify()

    # Dunder methods to allow: `with Semaphore(2):`
    def __enter__(self) -> 'Semaphore':
        self.acquire()
        return self

    def __exit__(
            self,
            exc_type: Type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None
    ) -> None:
        self.release()
