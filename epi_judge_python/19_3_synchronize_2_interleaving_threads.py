"""
#19.3 IMPLEMENT SYNCHRONIZATION FOR TWO INTERLEAVING THREADS

Thread t1 prints odd numbers from 1 to 10;
Thread t2 prints even numbers from 1 to 10.

Write code in which the two threads, running concurrently,
print the numbers from 1 to 10 in order.

Hint: The two threads need to notify each other when they are done.

Solution: A brute-force solution is to use a lock which is repeatedly captured
by the threads. A single variable, protected by the lock, indicates who went
last. The drawback of this approach is that it employs the busy waiting
antipattern: processor time that could be used to execute a different task is
instead wasted on useless activity.

Below we present a solution based on the same idea, but one that avoids busy
locking by using <what?>
"""

import threading


class TurnMonitor:
    """A monitor to coordinate thread turns using composition."""

    def __init__(self):
        self._condition = threading.Condition()
        self._is_odd_turn = True  # True for Odd, False for Even

    def wait_turn(self, desired_turn: bool) -> None:
        with self._condition:
            while self._is_odd_turn != desired_turn:
                self._condition.wait()

    def toggle_turn(self) -> None:
        with self._condition:
            self._is_odd_turn = not self._is_odd_turn
            self._condition.notify()


class NumberPrinterThread(threading.Thread):
    def __init__(self, turn_monitor: TurnMonitor, is_odd: bool, max_val: int):
        super().__init__()
        self._monitor = turn_monitor
        self._is_odd = is_odd
        self._max_val = max_val
        # Determine start value based on thread type
        self._start = 1 if is_odd else 2

    def run(self) -> None:
        for i in range(self._start, self._max_val + 1, 2):
            self._monitor.wait_turn(self._is_odd)

            try:
                # Production code would use logging here
                print(i)
            finally:
                # Ensures the other thread isn't deadlocked if print() fails
                self._monitor.toggle_turn()


if __name__ == '__main__':
    MAX_LIMIT = 10
    monitor = TurnMonitor()

    # By passing parameters, we reuse the same thread class
    odd_thread = NumberPrinterThread(monitor, is_odd=True, max_val=MAX_LIMIT)
    even_thread = NumberPrinterThread(monitor, is_odd=False, max_val=MAX_LIMIT)

    odd_thread.start()
    even_thread.start()

    odd_thread.join()
    even_thread.join()
