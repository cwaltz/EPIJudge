import threading
import time
import random
from typing import Any
from concurrent.futures import ThreadPoolExecutor


class MVCCStore:
    """
    A simple thread-safe Multi-Version Concurrency Control (MVCC) Key-Value
    Store.

    Demonstrates how modern databases (Postgres) handle the
    readers-writers problem without locking readers.
    """

    def __init__(self):
        # Storage format: key -> list of (transaction_id, value)
        # Using a built-in dict, list, and tuple per modern PEP 585 standards.
        self._data: dict[str, list[tuple[int, Any]]] = {}

        # Global Transaction ID allocator
        self._global_tx_id = 0
        self._tx_lock = threading.Lock()

        # Protects dictionary mutations (adding new keys or appending versions)
        self._write_lock = threading.Lock()

    def begin_transaction(self) -> int:
        """Assigns a monotonically increasing transaction ID."""
        with self._tx_lock:
            self._global_tx_id += 1
            return self._global_tx_id

    def read(self, tx_id: int, key: str) -> Any | None:
        """
        Snapshot Read: Finds the most recent version of a key that was
        committed *before or exactly when* this transaction started.

        Notice there is NO lock acquired here. Readers do not block writers.
        """
        # In Python, dictionary lookup and list iteration are GIL-safe atomic
        # operations.
        # We grab the reference to the list of versions.
        versions = self._data.get(key)
        if not versions:
            return None

        # Iterate backwards to find the latest version visible to this
        # transaction
        for commit_tx_id, value in reversed(versions):
            if commit_tx_id <= tx_id:
                return value

        return None

    def write(self, tx_id: int, key: str, value: Any) -> None:
        """
        Appends a new version of the data.
        It does not overwrite existing data, ensuring active readers
        can still see the snapshot they started with.
        """
        with self._write_lock:
            if key not in self._data:
                self._data[key] = []

            # Append the new version. Writers only block other Writers for the
            # microsecond it takes to append to the list.
            self._data[key].append((tx_id, value))

    def vacuum(self, oldest_active_tx_id: int) -> int:
        """
        Garbage Collection (Compaction):
        Removes stale versions that are no longer visible to any active
        transaction.
        Essential for Staff-level completeness (prevents OOM errors in
        long-running systems).
        """
        cleaned_count = 0
        with self._write_lock:
            for key, versions in self._data.items():
                # We need to keep the most recent version that is
                # <= oldest_active_tx_id and everything newer.
                keep_idx = 0
                for i in range(len(versions) - 1, -1, -1):
                    if versions[i][0] <= oldest_active_tx_id:
                        keep_idx = i
                        break

                # Slice the list to remove unreachable old versions
                if keep_idx > 0:
                    cleaned_count += keep_idx
                    self._data[key] = versions[keep_idx:]

        return cleaned_count

    def debug_state(self) -> dict[str, list[tuple[int, Any]]]:
        """
        Returns a snapshot of the internal state for demonstration & debugging.
        Properly encapsulates the protected _data member.
        """
        with self._write_lock:
            # Return a shallow copy of the dictionary to prevent external
            # mutation
            return {k: list(v) for k, v in self._data.items()}


# ==========================================
# Execution and Demonstration
# ==========================================

def simulate_reader(worker_id: int, store: MVCCStore):
    """Simulates a long-running read transaction."""
    tx_id = store.begin_transaction()
    print(f"[Reader {worker_id}] Started Tx {tx_id}. Taking a snapshot...")

    # Simulate work/delay to allow writers to mutate data while reading
    time.sleep(random.uniform(0.1, 0.5))

    # Reader should see the state of the database exactly as it was when Tx
    # started
    val1 = store.read(tx_id, "account_balance")
    print(f"[Reader {worker_id}] (Tx {tx_id}) Read account_balance: {val1}")


def simulate_writer(worker_id: int, store: MVCCStore, new_val: int):
    """Simulates a write transaction updating the state."""
    time.sleep(random.uniform(0.05, 0.2))  # Stagger start times
    tx_id = store.begin_transaction()

    print(
        f"[Writer {worker_id}] (Tx {tx_id}) Writing account_balance = "
        f"{new_val}")
    store.write(tx_id, "account_balance", new_val)


if __name__ == '__main__':
    db = MVCCStore()

    # Initialize baseline data
    init_tx = db.begin_transaction()
    db.write(init_tx, "account_balance", 100)
    print(f"[System] Initialized account_balance to 100 at Tx {init_tx}\n")

    # Run readers and writers concurrently
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Start a reader. It will pause mid-transaction.
        executor.submit(simulate_reader, 1, db)

        # While the reader is paused, fire off several writers
        executor.submit(simulate_writer, 1, db, 200)
        executor.submit(simulate_writer, 2, db, 300)

        # Start another reader later to see the updated state
        time.sleep(0.3)
        executor.submit(simulate_reader, 2, db)

    # Demonstrate Vacuum / Compaction
    print("\n[System] Database state before Vacuum:")
    print(db.debug_state())

    # Assume the oldest active transaction is now Tx 4
    removed = db.vacuum(oldest_active_tx_id=4)
    print(f"\n[System] Vacuumed {removed} stale versions.")
    print("[System] Database state after Vacuum:")
    print(db.debug_state())
