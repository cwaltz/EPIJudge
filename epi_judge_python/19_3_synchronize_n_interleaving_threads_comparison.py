"""
#19.3 IMPLEMENT SYNCHRONIZATION FOR N INTERLEAVING THREADS

The Shared Counter Benchmark

To actually see the massive performance difference between the Minimal and
Monolithic locking strategies, we need a scenario where threads are allowed
to work concurrently.

Instead of strict turns, we will use a Shared Counter (like a task queue).
Threads will safely grab the next available number and then process it (sleep).

Here is a single, combined script that runs both strategies back-to-back so
you can see the difference immediately.

What you will see when you run this:

Monolithic Time: ~7.5 seconds.
(15 tasks * 0.5 seconds). The threads execute strictly one at a time because
the lock is held during the sleep.

Minimal Time: ~2.5 seconds.
The lock is only held for a microsecond to increment the counter. All 3 threads
spend their 0.5 seconds sleeping at the same time.

This proves why minimizing the critical section is vital for application
throughput.
"""

import threading
import time

MAX_LIMIT = 15
NUM_THREADS = 3
IO_DELAY = 0.5  # Simulating half a second of network/disk I/O


class ThreadSafeCounter:
    def __init__(self):
        self.value = 1
        self.lock = threading.Lock()


# ==========================================
# STRATEGY 1: MONOLITHIC (The Anti-Pattern)
# ==========================================
def worker_monolithic(counter: ThreadSafeCounter, thread_id: int):
    while True:
        # 1. Acquire Lock
        with counter.lock:
            if counter.value > MAX_LIMIT:
                break

            my_val = counter.value
            counter.value += 1

            # 2. DO I/O WHILE HOLDING THE LOCK
            print(f"[Monolithic] Thread-{thread_id} processing {my_val}")
            time.sleep(IO_DELAY)
        # 3. Release Lock


# ==========================================
# STRATEGY 2: MINIMAL (The Industry Standard)
# ==========================================
def worker_minimal(counter: ThreadSafeCounter, thread_id: int):
    while True:
        # 1. Acquire Lock
        with counter.lock:
            if counter.value > MAX_LIMIT:
                break

            my_val = counter.value
            counter.value += 1
        # 2. RELEASE LOCK IMMEDIATELY

        # 3. DO I/O WITHOUT THE LOCK
        print(f"[Minimal] Thread-{thread_id} processing {my_val}")
        time.sleep(IO_DELAY)


def run_benchmark(strategy_func, name: str):
    counter = ThreadSafeCounter()
    threads = []

    start_time = time.perf_counter()

    for i in range(NUM_THREADS):
        t = threading.Thread(target=strategy_func, args=(counter, i))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    execution_time = time.perf_counter() - start_time
    print(f"\n---> {name} Execution time: {execution_time:.4f} seconds\n")
    print("-" * 50)


if __name__ == '__main__':
    print("Starting Monolithic Benchmark (Holding lock during I/O)...")
    run_benchmark(worker_monolithic, "MONOLITHIC")

    print("Starting Minimal Benchmark (Releasing lock before I/O)...")
    run_benchmark(worker_minimal, "MINIMAL")
