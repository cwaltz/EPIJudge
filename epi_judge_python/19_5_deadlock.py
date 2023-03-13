"""
19.5 DEADLOCK

When threads need to acquire multiple locks to enter a critical section,
deadlock can result. As an example, suppose both T1 & T2 need to acquire locks
L & M. If T1 first acquires L, & then T2 then acquires M, they end up waiting on
each other forever.

Identify a concurrency bug in the program below, & modify the code to resolve
the issue.
"""

import threading


class Account:
    _global_id = 0

    def __init__(self, balance):
        self.balance = balance
        self.id = Account._global_id
        Account._global_id += 1
        self.lock = threading.RLock()

    def get_balance(self):
        return self.balance

    @staticmethod
    def transfer(acc_from, acc_to, amount):
        th = threading.Thread(target=acc_from.move, args=(acc_to, amount))
        th.start()

    def _move(self, acc_to, amount):
        with self.lock:
            if amount > self.balance:
                return False
            acc_to.balance += amount
            self.balance -= amount
            print('returning True')
            return True

    def _move_modified(self, acc_to, amount):  # Solution resolving the issue
        lock1 = self.lock if self.id < acc_to.id else acc_to.lock
        lock2 = acc_to.lock if self.id < acc_to.id else self.lock
        # Does not matter if lock1 equals lock2:
        # since recursive_mutex locks are reentrant, we will re-acquire lock2.
        with lock1, lock2:
            if amount > self.balance:
                return False
            acc_to.balance += amount
            self.balance -= amount
            print('returning True')
            return True


"""
Solution:

Suppose U1 initiates a transfer to U2, & immediately afterwards, U2 initiates a
transfer to U1. Since each transfer takes place in a separate thread, it's
possible for the first thread to lock U1 & then the second thread to be 
scheduled in & take the lock U2. The program is now deadlocked - each of the two
threads is waiting for the lock held by the other thread.

One solution is to have a global lock which is acquired by the transfer method.
The drawback is that it blocks transfers that are unrelated, e.g., U3 cannot 
transfer to U4 if there is a pending transfer from U5 to U6.

The canonical way to avoid deadlock is to have a global ordering on locks & 
acquire them in that order. Since accounts have a unique integer id, the update
below is all that is needed to solve the deadlock.
"""
