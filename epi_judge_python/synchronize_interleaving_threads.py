"""
#19.3 IMPLEMENT SYNCHRONIZATION FOR TWO INTERLEAVING THREADS

Thread t1 prints odd numbers from 1 to 100; Thread t2 prints even numbers
from 1 to 100.

Write code in which the two threads, running concurrently, print the numbers
from 1 to 100 in order.

Hint: The two threads need to notify each other when they are done.

Solution: A brute-force solution is to use a lock which is repeatedly
captured by the threads. A single variable, protected by the lock, indicates
who went last. The drawback of this approach is that it employs the busy
waiting antipattern: processor time that could be used to execute a different
task is instead wasted on useless activity.

Below we present a solution based on the same idea, but one that avoids busy
locking by using <what?>
"""

import threading


class OddEvenMonitor(threading.Condition):
    ODD_TURN = True
    EVEN_TURN = False

    def __init__(self):
        super().__init__()
        self.turn = self.ODD_TURN

    def wait_turn(self, old_turn):
        with self:
            while self.turn != old_turn:
                self.wait()

    def toggle_turn(self):
        with self:
            self.turn ^= True
            self.notify()


class OddThread(threading.Thread):
    def __init__(self, monitor):
        super().__init__()
        self.monitor = monitor

    def run(self):
        for i in range(1, 101, 2):
            self.monitor.wait_turn(OddEvenMonitor.ODD_TURN)
            print(i)
            self.monitor.toggle_turn()


class EvenThread(threading.Thread):
    def __init__(self, monitor):
        super().__init__()
        self.monitor = monitor

    def run(self):
        for i in range(2, 101, 2):
            self.monitor.wait_turn(OddEvenMonitor.EVEN_TURN)
            print(i)
            self.monitor.toggle_turn()
