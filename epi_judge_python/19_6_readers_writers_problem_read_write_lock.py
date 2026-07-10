import threading
import time
import random
from typing import Any
from concurrent.futures import ThreadPoolExecutor


class ReaderLockContext:
    """Idiomatic context manager for read operations."""

    def __init__(self, rw_lock: "ReadWriteLock") -> None:
        self.rw_lock = rw_lock

    def __enter__(self) -> None:
        self.rw_lock.acquire_read()

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.rw_lock.release_read()


class WriterLockContext:
    """Idiomatic context manager for write operations."""

    def __init__(self, rw_lock: "ReadWriteLock") -> None:
        self.rw_lock = rw_lock

    def __enter__(self) -> None:
        self.rw_lock.acquire_write()

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.rw_lock.release_write()


class ReadWriteLock:
    """
    A thread-safe, production-ready Read-Write Lock implementing Writer
    Preference.
    Provides explicit context managers (`.reader`, `.writer`) as well as
    public manual acquire/release methods.
    """

    def __init__(self) -> None:
        # Internal state is strictly protected
        self._monitor = threading.Condition()
        self._readers = 0
        self._waiting_writers = 0
        self._writer_active = False

        # Expose idiomatic sub-lock handles
        self.reader = ReaderLockContext(self)
        self.writer = WriterLockContext(self)

    # ==========================================
    # Public API for Manual Lock Management
    # ==========================================

    def acquire_read(self) -> None:
        """Acquires the read lock, waiting if a writer is active or queued."""
        with self._monitor:
            while self._writer_active or self._waiting_writers > 0:
                self._monitor.wait()
            self._readers += 1

    def release_read(self) -> None:
        """
        Releases the read lock. Wakes waiting threads if it's the last reader.
        """
        with self._monitor:
            self._readers -= 1
            if self._readers == 0:
                self._monitor.notify_all()

    def acquire_write(self) -> None:
        """
        Acquires the exclusive write lock, waiting for active readers to finish.
        """
        with self._monitor:
            self._waiting_writers += 1
            try:
                while self._writer_active or self._readers > 0:
                    self._monitor.wait()
            except Exception:
                self._waiting_writers -= 1
                raise

            self._waiting_writers -= 1
            self._writer_active = True

    def release_write(self) -> None:
        """Releases the write lock and wakes all waiting threads."""
        with self._monitor:
            self._writer_active = False
            self._monitor.notify_all()


# ==========================================
# Reusable Production-Style Target Class
# ==========================================

class ThreadSafeSharedResource:
    """
    Demonstrates encapsulation of business data using our custom ReadWriteLock.
    """

    def __init__(self) -> None:
        self._rw_lock = ReadWriteLock()
        self._shared_data = 0

    def read_metric(self) -> int:
        # Using the clean context manager syntax
        # (calls acquire_read / release_read safely)
        with self._rw_lock.reader:
            return self._shared_data

    def update_metric(self, value: int) -> None:
        # Using the clean context manager syntax
        # (calls acquire_write / release_write safely)
        with self._rw_lock.writer:
            self._shared_data += value


# ==========================================
# Execution Loop / Verification
# ==========================================

def run_reader(worker_id: int, resource: ThreadSafeSharedResource) -> None:
    for _ in range(2):
        time.sleep(random.uniform(0.05, 0.1))
        data = resource.read_metric()
        print(f"[Reader {worker_id}] Fetched current resource value: {data}")


def run_writer(worker_id: int, resource: ThreadSafeSharedResource) -> None:
    for _ in range(2):
        time.sleep(random.uniform(0.08, 0.15))
        increment = random.randint(1, 10)
        resource.update_metric(increment)
        print(
            f"--> [Writer {worker_id}] Incremented resource state "
            f"by +{increment}")


if __name__ == "__main__":
    shared_resource = ThreadSafeSharedResource()
    print("[System] Starting lock contention execution...\n")

    with ThreadPoolExecutor(max_workers=8) as executor:
        for i in range(3):
            executor.submit(run_reader, worker_id=i, resource=shared_resource)
            executor.submit(run_writer, worker_id=i, resource=shared_resource)

        time.sleep(0.5)
        executor.submit(run_reader, worker_id=99, resource=shared_resource)
