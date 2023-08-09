"""
#19.8 IMPLEMENT A TIMER CLASS

Consider a web-based calendar in which the server hosting the calendar has to
perform a task when the next calendar event takes place. (The task could be
sending an email or a Short Message Service (SMS).) Your job is to design a
facility that manages the execution of such tasks.

Develop a timer class that manages the execution of deferred tasks. The timer
constructor takes as its argument an object which includes a run method and
a string-valued name field. The class must support -
(1.) starting a thread, identified by name, at a given time in the future; and
(2.) canceling a thread, identified by name (the cancel request is to be ignored
if the thread has already started).

Hint: There are two aspects - data structure design and concurrency.

Solution: The two aspects to the design are the data structures and the locking
mechanism.

We use two data structures. The first is a min-heap in which we insert
key-value pairs: the keys are run times and the values are the thread to run
at that time. A dispatch thread runs these threads; it sleeps from call to
call and may be woken up if a thread is added to or deleted from the pool. If
woken up, it advances or retards its remaining sleep time based on the top of
the min-heap. On waking up, it looks for the thread at the top of the
min-heap - if its launch time is the current time, the dispatch thread deletes
it from the min-heap and executes it. It then sleeps till the launch time for
the next thread in the min-heap. ( Because of deletions, it may happen that
the dispatch thread wakes up and finds nothing to do.)

The second data structure is a hash table with thread ids as keys and entries
in the min-heap as values. If we need to cancel a thread, we go to the
min-heap and delete it. Each time a thread is added, we add it to the
min-heap; if the insertion is to the top of the min-heap, we interrupt the
dispatch thread so that it can adjust its wake-up time.

Since the min-heap is shared by the update methods and the dispatch thread,
we need to lock it. The simplest solution is to have a single lock that is
used for all read and writes into the min-heap and the hash table.
"""

from enum import Enum
from heapq import heappush
from time import time
from threading import Thread

NOW = time()


class TaskStatus(Enum):
    WAITING = 1
    STARTED = 2
    CANCELED = 3


class Task(Thread):
    def __init__(self, name: str, start_time: float):
        super().__init__()
        self.name = name
        self.start_time = start_time
        self.status = TaskStatus.WAITING

    def __lt__(self, other: 'Task') -> bool:
        return self.start_time < other.start_time

    def run(self) -> None:
        print(f'Task {self.name} with start time: {self.start_time} started '
              f'at {time()}')
        self.status = TaskStatus.STARTED


class Timer:
    def __init__(self):
        self._min_heap = []  # Stores tasks
        self._mapping = {}  # Stores <task name, task> items

    def cancel_task(self, task_name: str):
        if task_name not in self._mapping:
            raise Exception(f'Task: {task_name} not found')
        task = self._mapping[task_name]
        if task.status == TaskStatus.STARTED:
            print(f'Task: {task_name} has already started. Ignoring the cancel '
                  f'request.')
        elif task.status == TaskStatus.CANCELED:
            print(f'Task: {task_name} has already been canceled.')
        else:  # if task.status == TaskStatus.WAITING:
            print(f'Canceling Task: {task_name}.')
            task.status = TaskStatus.CANCELED
            self._mapping[task_name] = task

    def add_task(self, task: Task):
        if task.name in self._mapping:
            raise Exception(f'Task: {task.name} is already present.')
        heappush(self._min_heap, task)
        self._mapping[task.name] = task


class Dispatcher(Thread):
    def __init__(self, timer: Timer):
        super().__init__()
        self._timer = timer

    def run(self) -> None:
        pass


# TODO: To be completed yet!
