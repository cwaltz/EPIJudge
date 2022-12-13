import collections
import functools
import heapq
from typing import List

from test_framework import generic_test
from test_framework.test_utils import enable_executor_hook

# Event is a tuple (start_time, end_time)
Event = collections.namedtuple('Event', ('start', 'finish'))


def find_max_simultaneous_events(events: List[Event]) -> int:
    """
    13.6

    Time complexity = O(n log n), where n is the number of events.
    Space complexity = O(n)

    Source: Official leetcode solution :)
    Approach 1: Priority Queues
    https://leetcode.com/problems/meeting-rooms-ii/solutions/168762/meeting-rooms-ii/

    Similar to Leetcode # 253

    Only 7 lines of code! :)

    Test PASSED (97/97) [  11 ms]
    Average running time:  126 us
    Median running time:     3 us
    """
    # The heap initialization
    free_rooms = []

    # Sort the events in increasing order of their start time.
    events.sort(key=lambda x: x[0])

    # For all the remaining meeting rooms
    for event in events:

        # If the room due to free up the earliest is free, assign that room
        # to this meeting.
        if free_rooms and free_rooms[0] < event[0]:
            heapq.heappop(free_rooms)

        # If a new room is to be assigned, then also we add to the heap.
        # If an old room is allocated, then also we have to add to the heap
        # with updated end time.
        heapq.heappush(free_rooms, event[1])

    # The size of the heap tells us the minimum rooms required for all the
    # meetings.
    return len(free_rooms)


def find_max_simultaneous_events_neetcode(events: List[Event]) -> int:
    """
    Time complexity = O(n log n), where n is the number of events.
    Space complexity = O(n)

    Test PASSED (97/97) [  14 ms]
    Average running time:  162 us
    Median running time:     5 us
    """
    start_times = sorted([event.start for event in events])
    finish_times = sorted([event.finish for event in events])

    max_num_simultaneous_events = num_simultaneous_events = 0
    start_index = finish_index = 0
    while start_index < len(events):
        if start_times[start_index] <= finish_times[finish_index]:
            start_index += 1
            num_simultaneous_events += 1
        else:
            finish_index += 1
            num_simultaneous_events -= 1
        if max_num_simultaneous_events < num_simultaneous_events:
            max_num_simultaneous_events = num_simultaneous_events
    return max_num_simultaneous_events


def find_max_simultaneous_events_namedtuple(events: List[Event]) -> int:
    """
    Time complexity = O(n log n), where n is the number of events.
    Space complexity = O(n)

    Test PASSED (97/97) [  42 ms]
    Average running time:  504 us
    Median running time:    48 us
    """
    # Endpoint is a tuple (start_time, 0) or (end_time, 1) so that if times are
    # equal, start_time comes first.
    Endpoint = collections.namedtuple('Endpoint', ('time', 'is_start'))
    # Builds an array of all endpoints.
    endpoints = [
        e
        for event in events
        for e in (Endpoint(event.start, True), Endpoint(event.finish, False))
    ]
    # Sorts the endpoint array according to the time,
    # breaking ties by putting start times before end times.
    endpoints.sort(key=lambda endpoint: (endpoint.time, not endpoint.is_start))

    # Track the number of simultaneous events,
    # record the maximum number of simultaneous events.
    max_num_simultaneous_events, num_simultaneous_events = 0, 0
    for e in endpoints:
        if e.is_start:
            num_simultaneous_events += 1
            if max_num_simultaneous_events < num_simultaneous_events:
                max_num_simultaneous_events = num_simultaneous_events
        else:
            num_simultaneous_events -= 1
    return max_num_simultaneous_events


def find_max_simultaneous_events_with_tuple(events: List[Event]) -> int:
    """
    Time complexity = O(n log n), where n is the number of events.
    Space complexity = O(n)

    Test PASSED (97/97) [  32 ms]
    Average running time:  351 us
    Median running time:     7 us
    """
    endpoints = [
        endpoint
        for event in events
        for endpoint in ((event.start, True), (event.finish, False))
    ]
    endpoints.sort(key=lambda endpoint: (endpoint[0], not endpoint[1]))
    max_num_simultaneous_events, num_simultaneous_events = 0, 0
    for endpoint in endpoints:
        if endpoint[1]:
            num_simultaneous_events += 1
            if max_num_simultaneous_events < num_simultaneous_events:
                max_num_simultaneous_events = num_simultaneous_events
        else:
            num_simultaneous_events -= 1
    return max_num_simultaneous_events


@enable_executor_hook
def find_max_simultaneous_events_wrapper(executor, events):
    events = [Event(*x) for x in events]
    return executor.run(functools.partial(find_max_simultaneous_events,
                                          events))


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('calendar_rendering.py',
                                       'calendar_rendering.tsv',
                                       find_max_simultaneous_events_wrapper))
