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
    #13.6

    Time complexity = O(n log n), where n is the number of events.
    Space complexity = O(n)

    Source: Official leetcode solution :)
    Approach 2: Chronological Ordering
    https://leetcode.com/problems/meeting-rooms-ii/solutions/168762/meeting-rooms-ii/

    Similar to Leetcode # 253

    Only 11 lines of code! :)

    Test PASSED (97/97) [  9 ms]
    Average running time:  108 us
    Median running time:     3 us
    """
    start_timings = sorted([i[0] for i in events])  # O(n log n)
    end_timings = sorted(i[1] for i in events)  # O(n log n)
    num_of_events = len(events)
    start_index = end_index = used_rooms = 0
    while start_index < num_of_events:  # O(n)
        if start_timings[start_index] > end_timings[end_index]:
            # One of the meetings ends by the start of current meeting so
            # increment end_index & reuse that room for current meeting.
            # No need to increment used_rooms.
            end_index += 1
        else:  # start_timings[start_index] < end_timings[end_index]
            # All existing rooms are occupied so use a new room for current
            # meeting & increment used_rooms.
            used_rooms += 1
        start_index += 1
    return used_rooms


def find_max_simultaneous_events_using_heap(events: List[Event]) -> int:
    """
    Time complexity = O(n log n), where n is the number of events.
    Space complexity = O(n)

    Source: Official leetcode solution :)
    Approach 1: Priority Queues
    https://leetcode.com/problems/meeting-rooms-ii/solutions/168762/meeting-rooms-ii/

    Only 8 lines of code! :)

    Test PASSED (97/97) [  10 ms]
    Average running time:  115 us
    Median running time:     3 us
    """
    min_heap = []  # To store event end times
    events.sort(key=lambda x: x[0])  # Non-decreasing order of event start times
    for event in events:
        if min_heap and min_heap[0] < event[0]:
            # An event room becomes free before the current event starts so
            # assign that room to current event
            heapq.heapreplace(min_heap, event[1])  # Pop & return the smallest
            # item from the heap, & also push the new item. The heap size
            # doesn't change. If the heap is empty, IndexError is raised.
        else:
            # Either min_heap is empty or all old rooms are occupied so assign a
            # new room to current event
            heapq.heappush(min_heap, event[1])
    # Size of the heap tells us the minimum rooms required for all the events
    return len(min_heap)


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
