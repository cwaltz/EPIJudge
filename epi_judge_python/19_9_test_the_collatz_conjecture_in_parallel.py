"""
#19.9 TEST THE COLLATZ CONJECTURE IN PARALLEL

In Problem 12.11 on Page 176 & its solution we introduced the Collatz conjecture
& heuristics for checking it. In this problem, you are to build a parallel
checker for the Collatz conjecture.

Specifically, assume your program will run on a multicore machine, & threads in
your program will be distributed across the cores. Your program should check the
Collatz conjecture for every integer in [1, U] where U is an input to your
program.

Design a multi-threaded program for checking the Collatz conjecture. Make full
use of the cores available to you. To keep your program from overloading the
system, you should not have more than r threads running at a time.


Hint: Use multithreading for performance - take care to minimize threading
overhead.


Solution: Heuristics for pruning checks on individual integers are discussed in
Solution 12.11 on Page 176. The aim of this problem is implementing a
multi-threaded checker. We could have a master thread launch n threads, one per
number, starting with 1,2,...,x. The master thread would keep track of what
number needs to be processed next, & when a thread returned, it could re-assign
it the next unchecked number.

The problem with this approach is that the time spent executing the check in an
individual thread is very small compared to the overhead of communicating with
the thread. The natural solution is to have each thread process a subrange of
[1, U]. We could do this by dividing [1, U] into n equal sized sub-ranges, and
having Thread i handle the i_th subrange.

The heuristics for checking the Collatz conjecture take longer on some integers
than others, & in the strategy above there is the potential of a situation
arising where one thread takes much longer to complete than the others, which
leads to most of the cores being idle.

A good compromise is to have threads handle smaller intervals, which are still
large enough to offset the thread overhead. We can maintain a work-queue
consisting of unprocessed intervals, & assigning these to returning threads.
"""

import concurrent.futures


# Performs basic unit of work
def worker(lower, upper):
    for i in range(lower, upper + 1):
        assert collatz_check(i, set())
    print('(%d, %d)' % (lower, upper))


# Checks an individual number
def collatz_check(x, visited):
    if x == 1:
        return True
    elif x in visited:
        return False
    visited.add(x)
    if x & 1:  # odd number
        return collatz_check(3 * x + 1, visited)
    else:  # even number
        return collatz_check(x >> 1, visited)  # divide by 2


N = 100
NTHREADS = 10
RANGESIZE = 10

# Uses the library thread pool for task assignment and load balancing
executor = concurrent.futures.ProcessPoolExecutor(max_workers=NTHREADS)
with executor:
    for i in range(N // RANGESIZE):
        executor.submit(worker, i * RANGESIZE + 1, (i + 1) * RANGESIZE)
