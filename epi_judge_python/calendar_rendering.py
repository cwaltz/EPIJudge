import functools
import heapq
from typing import NamedTuple

from test_framework import generic_test
from test_framework.test_utils import enable_executor_hook


# Event is a tuple (start_time, end_time)
# Event = collections.namedtuple('Event', ('start', 'end'))
class Event(NamedTuple):
    start: int
    end: int


# collections.namedtuple('Endpoint', ('time', 'is_start'))
class Endpoint(NamedTuple):
    time: int
    is_start: bool


def find_max_simultaneous_events_sweep(events: list[Event]) -> int:
    """
    The sweep-line is an architectural pattern favored for its mental
    simplicity and extensibility (like if we added weights to the events)

    Test PASSED (97/97) [  27 ms]
    Average running time:  291 us
    Median running time:     5 us
    """
    time_points = []

    for event in events:
        # We assign +1 for a room being occupied,
        # and -1 for a room being vacated.
        time_points.append((event.start, 1))
        time_points.append((event.end, -1))

    # Sort the points.
    # The lambda function sorts primarily by time (x[0] ascending).
    # If times are tied, it sorts by the change value (x[1] descending).
    # Sorting descending for the tie-breaker ensures that +1 (starts) are
    # processed BEFORE -1 (ends) if they happen at the exact same millisecond.
    # This matches your original logic where start <= end counts as an overlap.
    time_points.sort(key=lambda x: (x[0], -x[1]))

    max_occupancy = 0
    curr_occupancy = 0

    # Sweep through the timeline chronologically
    for time, change in time_points:
        curr_occupancy += change
        if max_occupancy < curr_occupancy:
            max_occupancy = curr_occupancy

    return max_occupancy


def find_max_simultaneous_events(events: list[Event]) -> int:
    """
    Test PASSED (97/97) [  11 ms]
    Average running time:  125 us
    Median running time:     3 us
    """
    start_timings = sorted([event.start for event in events])
    end_timings = sorted([event.end for event in events])
    num_of_events = len(events)

    start_index, end_index = 0, 0
    max_occupancy, curr_occupancy = 0, 0
    while start_index < num_of_events:
        if start_timings[start_index] <= end_timings[end_index]:
            curr_occupancy += 1
            if max_occupancy < curr_occupancy:
                max_occupancy = curr_occupancy
            start_index += 1
        else:  # end_timings[end_index] < start_timings[start_index]
            curr_occupancy -= 1
            end_index += 1

    return max_occupancy


def find_max_simultaneous_events_shorter_faster(events: list[Event]) -> int:
    """
    #13.5

    Time complexity = O(n log n), where n is the number of events.
    Space complexity = O(n)

    Source: Official leetcode solution :)
    Approach 2: Chronological Ordering
    https://leetcode.com/problems/meeting-rooms-ii/solutions/168762/meeting-rooms-ii/

    Similar to Leetcode # 253

    Only 11 lines of code! :)

    Test PASSED (97/97) [  9 ms]
    Average running time:  102 us
    Median running time:     3 us
    """
    start_timings = sorted([i.start for i in events])  # O(n log n)
    end_timings = sorted(i.end for i in events)  # O(n log n)
    num_of_events = len(events)
    end_index = used_rooms = 0

    for start_index in range(num_of_events):  # O(n)
        if start_timings[start_index] <= end_timings[end_index]:
            used_rooms += 1
        else:  # start_timings[start_index] > end_timings[end_index]
            end_index += 1

    # # The above for loop replaced the below while loop
    # while start_index < num_of_events:  # O(n)
    #     if start_timings[start_index] <= end_timings[end_index]:
    #         # All existing rooms are occupied so use a new room for current
    #         # meeting & increment used_rooms.
    #         used_rooms += 1
    #     else:  # start_timings[start_index] > end_timings[end_index]:
    #         # One of the meetings ends by the start of current meeting so
    #         # increment end_index & reuse that room for current meeting.
    #         # No need to increment used_rooms.
    #         end_index += 1
    #
    #     start_index += 1

    return used_rooms


def find_max_simultaneous_events_using_heap(events: list[Event]) -> int:
    """
    Time complexity = O(n log n), where n is the number of events.
    Space complexity = O(n)

    Source: Official leetcode solution :)
    Approach 1: Priority Queues
    https://leetcode.com/problems/meeting-rooms-ii/solutions/168762/meeting-rooms-ii/

    Only 8 lines of code! :)

    Test PASSED (97/97) [  10 ms]
    Average running time:  115 us
    Median running time:     2 us
    """
    min_heap = []  # To store event end times
    events.sort(key=lambda e: e.start)
    # Non-decreasing order of event start times
    for event in events:
        if min_heap and min_heap[0] < event.start:
            # An event room becomes free before the current event starts so
            # assign that room to current event
            heapq.heapreplace(min_heap, event.end)  # Pop & return the smallest
            # item from the heap, & also push the new item. The heap size
            # doesn't change. If the heap is empty, IndexError is raised.
        else:
            # Either min_heap is empty or all old rooms are occupied so assign a
            # new room to current event
            heapq.heappush(min_heap, event.end)
    # Size of the heap tells us the minimum rooms required for all the events
    return len(min_heap)


@enable_executor_hook
def find_max_simultaneous_events_wrapper(executor, events):
    events = [Event(*x) for x in events]
    return executor.run(functools.partial(
        find_max_simultaneous_events_sweep, events))


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('calendar_rendering.py',
                                       'calendar_rendering.tsv',
                                       find_max_simultaneous_events_wrapper))
