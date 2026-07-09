"""
#19.3 IMPLEMENT SYNCHRONIZATION FOR N INTERLEAVING THREADS

For MAX_LIMIT = 15 and NUM_THREADS = 3,

Thread-0 prints 1, 4, 7, 10, 13;
Thread-1 prints 2, 5, 8, 11, 14;
Thread-2 prints 3, 6, 9, 12, 15;

Write code in which the n threads, running concurrently,
print the numbers from 1 to 15 in order.

Hint: The three threads need to notify the other two when they are done.

Solution: A brute-force solution is to use a lock which is repeatedly captured
by the threads. A single variable, protected by the lock, indicates who went
last. The drawback of this approach is that it employs the busy waiting
antipattern: processor time that could be used to execute a different task is
instead wasted on useless activity.

Below we present a solution based on the same idea, but one that avoids busy
locking by using <what?>
"""

import threading
import time


class TurnMonitor:
    """A monitor to coordinate turns among N threads."""

    def __init__(self, num_threads: int) -> None:
        self._condition = threading.Condition()
        self._current_turn = 0  # Replaced boolean with an integer counter
        self._num_threads = num_threads

    def wait_turn(self, thread_id: int) -> None:
        with self._condition:
            # Modulo arithmetic ensures threads cycle in order: 0, 1, 2... N-1
            while self._current_turn % self._num_threads != thread_id:
                self._condition.wait()

    def end_turn(self) -> None:
        with self._condition:
            self._current_turn += 1
            # CRITICAL: Must wake all threads for N > 2
            self._condition.notify_all()


class NumberPrinterThread(threading.Thread):
    def __init__(self, turn_monitor: TurnMonitor, thread_id: int,
                 num_threads: int, max_val: int) -> None:
        super().__init__()
        self._monitor = turn_monitor
        self._thread_id = thread_id
        self._num_threads = num_threads
        self._max_val = max_val

    def run(self) -> None:
        # Determine exactly which numbers this thread is responsible for.
        # Example for 3 threads:
        # Thread 0 prints 1, 4, 7...
        # Thread 1 prints 2, 5, 8...
        start_val = self._thread_id + 1

        for j in range(start_val, self._max_val + 1, self._num_threads):
            self._monitor.wait_turn(self._thread_id)

            try:
                # In production, use standard logging instead of print
                print(f"Thread-{self._thread_id}: {j}")
                time.sleep(1)
            finally:
                self._monitor.end_turn()


def main():
    MAX_LIMIT = 15
    NUM_THREADS = 3  # Easily scale to any number of threads

    monitor = TurnMonitor(num_threads=NUM_THREADS)
    threads = []

    start_time = time.perf_counter()

    # Initialize and start N threads dynamically
    for i in range(NUM_THREADS):
        t = NumberPrinterThread(
            monitor,
            thread_id=i,
            num_threads=NUM_THREADS,
            max_val=MAX_LIMIT
        )
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    end_time = time.perf_counter()
    execution_time = end_time - start_time

    print(f"Execution time: {execution_time:.4f} seconds")


if __name__ == '__main__':
    main()
