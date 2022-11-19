import functools
import heapq
import math
from typing import Iterator, List, Tuple

from test_framework import generic_test
from test_framework.test_utils import enable_executor_hook


class Star:
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x, self.y, self.z = x, y, z

    @property
    def distance(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def __lt__(self, rhs: 'Star') -> bool:
        return self.distance < rhs.distance

    def __repr__(self):
        return str(self.distance)

    def __str__(self):
        return self.__repr__()

    def __eq__(self, rhs):
        return math.isclose(self.distance, rhs.distance)


def find_closest_k_stars(stars: Iterator[Star], k: int) -> List[Star]:
    """
    #10.4

    Time complexity = O(n log k)
    Space complexity = O(k)

    Test PASSED (51/51) [  10 ms]
    Average running time:  291 us
    Median running time:    37 us
    """
    # max_heap to store the closest k stars seen so far.
    max_heap: List[Tuple[float, Star]] = []
    for star in stars:
        # Add each star to the max-heap. If the max-heap size exceeds k, remove
        # the maximum element from the max-heap. As python has only min-heap,
        # insert tuple (negative of distance, star) to sort in reversed distance
        # order.
        heapq.heappush(max_heap, (-star.distance, star))
        if len(max_heap) == k + 1:
            heapq.heappop(max_heap)

    # Iteratively extract from the max-heap, which yields the stars sorted from
    # furthest to closest.
    return [s[1] for s in heapq.nlargest(k, max_heap)]


def find_closest_k_stars_alternate(stars: Iterator[Star], k: int) -> List[Star]:
    """
    #10.4

    Time complexity = O(n log k)
    Space complexity = O(k)

    Test PASSED (51/51) [  10 ms]
    Average running time:  296 us
    Median running time:    38 us
    """
    max_heap: List[Tuple[float, Star]] = []
    for star in stars:
        heapq.heappush(max_heap, (-star.distance, star))
        if len(max_heap) == k + 1:
            heapq.heappop(max_heap)
    result = []
    while max_heap:
        result.append(heapq.heappop(max_heap)[1])
    return result


def comp(expected_output, output):
    if len(output) != len(expected_output):
        return False
    return all(
        math.isclose(s.distance, d)
        for s, d in zip(sorted(output), expected_output))


@enable_executor_hook
def find_closest_k_stars_wrapper(executor, stars, k):
    stars = [Star(*a) for a in stars]
    return executor.run(functools.partial(find_closest_k_stars, iter(stars),
                                          k))


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('k_closest_stars.py',
                                       'k_closest_stars.tsv',
                                       find_closest_k_stars_wrapper, comp))
