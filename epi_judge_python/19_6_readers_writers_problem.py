"""
#19.6 THE READERS-WRITERS PROBLEM

Consider an object s which is read from and written to by many threads.
(For example, s could be the cache from Problem 19.1 on Page 291.) You need to
ensure that no thread may access s for reading or writing while another
thread is writing to s. (Two or more readers may access s at the same time.)

One way to achieve this is by protecting s with a mutex that ensures that two
threads cannot access s at the same time. However, this solution is
suboptimal because it is possible that a reader R1 has locked s and another
reader R2 wants to access s. Reader R2 does not have to wait until R1 is done
reading; instead, R2 should start reading right away.

This motivates the first readers-writers problem: protect s with the added
constraint that no reader is to be kept waiting if s is currently opened for
reading.

Implement a synchronization mechanism for the first readers-writers problem.

Hint: Track the number of readers.

Solution: We want to keep track of whether the string is being read from,
as well as whether the string is being written to. Additionally, if the
string is being read from, we want to know the number of concurrent readers.
We achieve this with a pair of locks - a read lock and a write lock - and a read
counter locked by the read lock.

A reader proceeds as follows. It locks the read lock, increments the counter,
and releases the read lock. After it performs its reads, it locks the read lock,
decrements the counter, and releases the read lock. A writer locks the write
lock, then performs the following in an infinite loop. It locks the read lock,
checks to see if the read counter is 0; if so, it performs its write, releases
the read lock, and breaks out of the loop. Finally, it releases the write lock.
As in Solution 19.3 on Page 293, we use wait-notify primitives to avoid busy
waiting.
"""

# LR (read_lock) & LW (write_lock) are class attributes in the
# RW (ReaderWriter) class.
# They serve as read and write locks. The integer variable read_count in RW
# tracks the number of readers.

import threading


class ReaderWriter:
    def __init__(self, data: int = 0):
        self.data = data
        self.read_count = 0
        self.read_lock = threading.Condition()
        self.write_lock = threading.Condition()


class Reader(threading.Thread):

    def run(self, reader_writer: ReaderWriter = None):
        while True:
            with reader_writer.read_lock:
                reader_writer.read_count += 1

            print(reader_writer.data)
            with reader_writer.read_lock:
                reader_writer.read_count -= 1
                reader_writer.read_lock.notify()
            do_something_else()


class Writer(threading.Thread):

    def run(self, reader_writer: ReaderWriter = None):
        while True:
            with reader_writer.write_lock:
                done = False
                while not done:
                    with reader_writer.read_lock:
                        if reader_writer.read_count == 0:
                            reader_writer.data += 1
                            done = True
                        else:
                            # use wait/notify to avoid busy waiting
                            while reader_writer.read_count != 0:
                                reader_writer.read_lock.wait()
            do_something_else()


def do_something_else():
    raise NotImplementedError

#
# class Reader(threading.Thread):
#
#     def run(self, RW=None):
#         while True:
#             with RW.LR:
#                 RW.read_count += 1
#
#             print(RW.data)
#             with RW.LR:
#                 RW.read_count -= 1
#                 RW.LR.notify()
#             do_something_else()
#
#
# class Writer(threading.Thread):
#
#     def run(self, RW=None):
#         while True:
#             with RW.LW:
#                 done = False
#                 while not done:
#                     with RW.LR:
#                         if RW.read_count == 0:
#                             RW.data += 1
#                             done = True
#                         else:
#                             # use wait/notify to avoid busy waiting
#                             while RW.read_count != 0:
#                                 RW.LR.wait()
#             do_something_else()
#
#
# def do_something_else():
#     raise NotImplementedError
