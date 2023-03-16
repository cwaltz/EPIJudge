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


class Semaphore:
    def __init__(self, max_available: int):
        self._condition_variable = threading.Condition()
        self._MAX_AVAILABLE = max_available
        self._taken = 0

    def acquire(self) -> None:
        self._condition_variable.acquire()
        while self._taken == self._MAX_AVAILABLE:
            self._condition_variable.wait()
        self._taken += 1
        self._condition_variable.release()

        # Alternate implementation using 'with' statement
        # with self._condition_variable:
        #     while self._taken == self._MAX_AVAILABLE:
        #         self._condition_variable.wait()
        #     self._taken += 1

    def release(self) -> None:
        self._condition_variable.acquire()
        self._taken -= 1
        self._condition_variable.notify()
        self._condition_variable.release()

        # Alternate implementation using 'with' statement
        # with self._condition_variable:
        #     self._taken -= 1
        #     self._condition_variable.notify()
