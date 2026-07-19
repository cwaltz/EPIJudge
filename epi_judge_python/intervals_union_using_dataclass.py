import functools
import itertools
from dataclasses import dataclass

from test_framework import generic_test
from test_framework.test_utils import enable_executor_hook


@dataclass(frozen=True, slots=True)
class Endpoint:
    is_closed: bool
    val: int


@dataclass(frozen=True, slots=True)
class Interval:
    left: Endpoint
    right: Endpoint


def union_of_intervals_production(intervals: list[Interval]) -> list[Interval]:
    """
    #13.7

    Test PASSED (191/191) [  10 ms]
    Average running time:   68 us
    Median running time:     6 us
    """
    if not intervals:
        return []

    # 1. Use sorted() to avoid mutating the input parameter (Thread-safe)
    # Sort by left value ascending. If tied, closed endpoints come first.
    sorted_intervals = sorted(intervals,
                              key=lambda i: (i.left.val, not i.left.is_closed))

    result = [sorted_intervals[0]]

    # 2. Skip the first element to avoid redundant self-comparison
    for curr in itertools.islice(sorted_intervals, 1, None):
        prev = result[-1]

        # Extract boolean states for readability
        overlaps_strictly = curr.left.val < prev.right.val
        touches_exactly = curr.left.val == prev.right.val
        can_merge_touching = touches_exactly and (
                    curr.left.is_closed or prev.right.is_closed)

        if overlaps_strictly or can_merge_touching:
            # They overlap. Determine the new right endpoint.
            extends_strictly = curr.right.val > prev.right.val
            extends_by_closure = (curr.right.val == prev.right.val and
                                  not prev.right.is_closed and
                                  curr.right.is_closed)

            if extends_strictly or extends_by_closure:
                # Replace the last interval with the newly merged interval.
                # Because the dataclass is frozen, we must instantiate a new
                # Interval, which safely prevents side effects elsewhere in
                # the application.
                result[-1] = Interval(prev.left, curr.right)
        else:
            # No overlap, add as a distinct interval
            result.append(curr)

    return result


@enable_executor_hook
def union_of_intervals_wrapper(executor, intervals):
    intervals = [
        Interval(Endpoint(x[1], x[0]), Endpoint(x[3], x[2])) for x in intervals
    ]

    result = executor.run(functools.partial(union_of_intervals_production,
                                            intervals))

    return [(i.left.val, i.left.is_closed, i.right.val, i.right.is_closed)
            for i in result]


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('intervals_union.py',
                                       'intervals_union.tsv',
                                       union_of_intervals_wrapper))
