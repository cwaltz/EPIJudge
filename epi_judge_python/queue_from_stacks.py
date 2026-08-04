"""
Gemini chat thread has in-depth discussion and a few open points:
https://gemini.google.com/app/28d19f25948028a2
"""

import collections
import threading

from test_framework import generic_test
from test_framework.test_failure import TestFailure


class Queue:
    """
    #8.8

    This approach takes O(m) time for m operations, which can be seen from the
    fact that each element is pushed no more than twice and popped no more
    than twice.

    Time complexity = O(1) per operation (amortized)
    Space complexity = O(n) for n elements in the queue

    Test PASSED (65/65) [   2 ms]
    Average running time:   67 us
    Median running time:    18 us
    """

    def __init__(self) -> None:
        self._enq: list[int] = []
        self._deq: list[int] = []

    def enqueue(self, x: int) -> None:
        self._enq.append(x)

    def dequeue(self) -> int:
        self._ensure_deq_has_items()
        if not self._deq:
            raise IndexError('dequeue from empty queue')
        return self._deq.pop()

    def peek(self) -> int:
        self._ensure_deq_has_items()
        if not self._deq:
            raise IndexError('peek from empty queue')
        # Accessing [-1] is legal because it represents the top of the stack
        return self._deq[-1]

    def is_empty(self) -> bool:
        return not (self._enq or self._deq)

    def _ensure_deq_has_items(self) -> None:
        """
        Helper to lazily shift items from enq to deq.
        Abstracts the state mutation to keep dequeue and peek DRY.
        """
        if not self._deq:
            while self._enq:
                self._deq.append(self._enq.pop())


class CollectionsQueue:
    """
    Added only for benchmarking

    Test PASSED (65/65) [   1 ms]
    Average running time:   47 us
    Median running time:    12 us
    """

    def __init__(self) -> None:
        self._queue: collections.deque[int] = collections.deque()

    def enqueue(self, x: int) -> None:
        self._queue.append(x)

    def dequeue(self) -> int:
        return self._queue.popleft()


class ProductionQueue[T]:
    """
    A thread-safe Queue implementation using two stacks.

    Test PASSED (65/65) [   4 ms]
    Average running time:  118 us
    Median running time:    31 us
    """

    def __init__(self) -> None:
        self._enq: list[T] = []
        self._deq: list[T] = []
        # Reentrant lock to prevent race conditions during state mutations
        self._lock = threading.RLock()

    def enqueue(self, x: T) -> None:
        """Adds an item to the back of the queue."""
        with self._lock:
            self._enq.append(x)

    def dequeue(self) -> T:
        """Removes and returns the front item of the queue."""
        with self._lock:
            self._shift_stacks()
            if not self._deq:
                raise IndexError('dequeue from empty queue')
            return self._deq.pop()

    def peek(self) -> T:
        """Returns the front item without removing it."""
        with self._lock:
            self._shift_stacks()
            if not self._deq:
                raise IndexError('peek from empty queue')
            return self._deq[-1]

    def _shift_stacks(self) -> None:
        """Helper to transfer items if the dequeue stack is empty.
        Assumes the caller has acquired the lock."""
        if not self._deq:
            while self._enq:
                self._deq.append(self._enq.pop())

    def __bool__(self) -> bool:
        """Allows pythonic truthiness checks (e.g., `if queue:`)."""
        with self._lock:
            return bool(self._enq or self._deq)

    def __len__(self) -> int:
        """Returns the total number of items in the queue."""
        with self._lock:
            return len(self._enq) + len(self._deq)


"""
To solve the single-lock bottleneck in a two-stack queue, a staff-level 
engineer will move away from a monolithic lock and implement fine-grained 
locking.

Because our data structure is naturally split into two independent halves 
(a write stack and a read stack), we can use the Two-Lock Queue pattern. This 
allows producers (enqueue) and consumers (dequeue) to operate completely in 
parallel 99% of the time.

Here is the architectural breakdown of how to optimize this for highly 
concurrent workloads.

1. The Two-Lock Architecture
Instead of one lock guarding the whole object, we instantiate two separate 
locks:

_enq_lock: Exclusively guards the _enq stack.

_deq_lock: Exclusively guards the _deq stack.

The resulting concurrency behavior:

Producers only acquire _enq_lock. They never block consumers who are reading 
from a populated _deq stack.

Consumers only acquire _deq_lock to pop an item. They never block producers 
from adding new items.

Contention only occurs during the rare, amortized transfer phase when _deq is 
empty.

2. Preventing Deadlocks (Lock Ordering)
When _deq is empty, the consumer must acquire both locks to transfer elements 
from _enq to _deq. This introduces the classic deadlock risk if threads attempt 
to acquire multiple locks in different orders.

To prevent this, we must enforce strict lock hierarchy: any thread that needs 
both locks must always acquire _deq_lock first, then _enq_lock. Because enqueue 
never needs the _deq_lock, a circular wait condition is mathematically 
impossible.
"""


class HighlyConcurrentQueue[T]:
    """
    Test PASSED (65/65) [   4 ms]
    Average running time:  116 us
    Median running time:    32 us
    """

    def __init__(self) -> None:
        self._enq: list[T] = []
        self._deq: list[T] = []
        self._enq_lock = threading.Lock()
        self._deq_lock = threading.Lock()

    def enqueue(self, x: T) -> None:
        # Producers only block other producers
        with self._enq_lock:
            self._enq.append(x)

    def dequeue(self) -> T:
        # Consumers only block other consumers, unless transferring
        with self._deq_lock:
            self._ensure_deq_has_items()
            if not self._deq:
                raise IndexError('dequeue from empty queue')
            return self._deq.pop()

    def _ensure_deq_has_items(self) -> None:
        """Assumes caller already holds _deq_lock."""
        if not self._deq:
            # Acquire second lock following strict ordering
            with self._enq_lock:
                # Double-check inside the lock in case another thread
                # already transferred items while we were waiting
                while self._enq:
                    self._deq.append(self._enq.pop())


"""
3. Optimizing for "Read-Heavy" Workloads (Peek)
If "read-heavy" specifically means your application calls peek() thousands of 
times per second (perhaps polling state), the _deq_lock becomes a new 
bottleneck because multiple peek() threads will serialize each other.

To optimize this, you would upgrade _deq_lock to a Read-Write Lock (RWLock).

Reads (peek): Acquire the _deq Read Lock. Thousands of threads can peek 
simultaneously without blocking each other.

Writes (dequeue or transfers): Acquire the _deq Write Lock. This momentarily 
pauses the peekers while the state mutates, then immediately lets them resume.

(Note: Python's standard library does not include an RWLock, so in production, 
you would use a battle-tested library like fastrwlock or implement one using 
standard threading primitives).

4. The Real-World Reality Check
In a system design interview, acknowledging the limits of your own architecture 
is crucial.

If you build this in pure Python, the Global Interpreter Lock (GIL) will still 
prevent true multi-core parallelism for CPU-bound threads. While this two-lock 
structure eliminates logical contention (threads waiting on each other), the 
GIL still enforces interpreter contention (Python only executing one bytecode 
at a time).

For enterprise-scale, highly concurrent Python queues, the correct move is 
often abandoning bounded memory structures in favor of lock-free inter-process 
queues (like ZeroMQ), Redis-backed queues, or message brokers (Kafka/RabbitMQ) 
that operate completely outside the Python runtime.
"""


def queue_tester(ops):
    try:
        q = HighlyConcurrentQueue()  # Usage 1

        for (op, arg) in ops:
            if op == 'Queue':
                q = HighlyConcurrentQueue()  # Usage 2
            elif op == 'enqueue':
                q.enqueue(arg)
            elif op == 'dequeue':
                result = q.dequeue()
                if result != arg:
                    raise TestFailure('Dequeue: expected ' + str(arg) +
                                      ', got ' + str(result))
            else:
                raise RuntimeError('Unsupported queue operation: ' + op)
    except IndexError:
        raise TestFailure('Unexpected IndexError exception')


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('queue_from_stacks.py',
                                       'queue_from_stacks.tsv',
                                       queue_tester))
