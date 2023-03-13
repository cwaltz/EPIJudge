"""
#19.2 ANALYZE TWO UNSYNCHRONIZED INTERLEAVED THREADS

Threads t1 & t2 each increment an integer variable N times, as shown in the code
below. This program yields nondeterministic results. Usually, it prints 2N, but
sometimes it prints a smaller value. The problem is more pronounced for large N.
As a concrete example, on one run the program output 1320209 when N = 1000000
was specified at the command line.
"""

import threading

N = 1000000
counter = 0


def increment_thread():
    global counter
    for _ in range(N):
        counter += 1


t1 = threading.Thread(target=increment_thread)
t2 = threading.Thread(target=increment_thread)

t1.start()
t2.start()
t1.join()
t2.join()

print(counter)

"""
What are the maximum & minimum values that could be printed by the program as a
function of N?

Hint: Be as perverse as you can when scheduling the threads.


Solution: First, note that the increment code is unguarded, which opens up the
possibility of its value being determined by the order in which threads that 
write to it are scheduled by the thread scheduler.

The maximum value is 2N. This occurs when the thread scheduler runs one thread
to completion, followed by the other thread.

When N = 1, the minimum value for the count variable is 1: t1 reads, t2 reads,
t1 increments & writes, then t2 increments & writes. When N > 1, the final value
of the count variable must be at least 2. The reasoning is as follows. There are
two possibilities. A thread, call it T, performs a 
read-increment-write-read-increment-write without the other thread writing
between reads, in which case the written value is at least 2. If the other
thread now writes a 1, it has not yet completed, so it will increment at least
once more. Otherwise, T's second read returns a value of 1 or more (since the
other thread has performed at least one write).

The lower bound of 2 is achieved according to the following thread schedule:
- t1 loads the value of the counter, which is 0.
- t2 executes the loop N - 1 times.
- t1 doesn't know that the value of the counter changed and writes 1 to it.
- t2 loads the value of the counter, which is 1.
- t1 executes the loop for the remaining N - 1 iterations.
- t2 doesn't know that the value of the counter has changed, & writes 2 to the
counter.
"""
