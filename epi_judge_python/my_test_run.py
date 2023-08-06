"""
Synchronize 3 threads (print '1', '2', '3' in that order)
"""

from time import sleep
from threading import Condition, Thread


class TurnMonitor(Condition):

    def __init__(self):
        super().__init__()
        self._turn = 1

    def wait_for_turn(self, desired_turn: int) -> None:
        with self:
            if self._turn != desired_turn:
                self.wait()

    def increment_turn(self) -> None:
        with self:
            self._turn += 1
            self.notify()


class CustomThread(Thread):
    def __init__(self, monitor: TurnMonitor, turn: int):
        super().__init__()
        self._monitor = monitor
        self._TURN = turn

    def run(self):
        print(f'Thread {self._TURN} running')
        self._monitor.wait_for_turn(self._TURN)
        print(self._TURN)
        self._monitor.increment_turn()


def main():
    turn_monitor = TurnMonitor()
    thread_1 = CustomThread(turn_monitor, 1)
    thread_2 = CustomThread(turn_monitor, 2)
    thread_3 = CustomThread(turn_monitor, 3)
    thread_3.start()
    sleep(2)
    thread_2.start()
    sleep(2)
    thread_1.start()


if __name__ == '__main__':
    main()
