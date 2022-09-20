import collections
import functools
from typing import List

from test_framework import generic_test
from test_framework.test_failure import TestFailure
from test_framework.test_utils import enable_executor_hook

MPG = 20


# gallons[i] is the amount of gas in city i, and distances[i] is the
# distance city i to the next city.
def find_ample_city(gallons: List[int], distances: List[int]) -> int:
    """
    #17.6

    Time complexity = O(n), where n is the number of cities.
    Space complexity = O(1)

    Test PASSED (202/202) [   1 ms]
    Average running time:   18 us
    Median running time:     4 us
    """
    remaining_gallons, minimum_gallons, idx = 0, 0, 0
    for i in range(len(gallons)):
        if remaining_gallons <= minimum_gallons:
            minimum_gallons, idx = remaining_gallons, i
        remaining_gallons += (gallons[i] - distances[i] / MPG)
    return idx


def find_ample_city_alternate(gallons: List[int], distances: List[int]) -> int:
    """
    Test PASSED (202/202) [   1 ms]
    Average running time:   70 us
    Median running time:    45 us
    """
    remaining_gallons = 0
    CityAndRemainingGas = collections.namedtuple('CityAndRemainingGas',
                                                 ('city', 'remaining_gallons'))
    city_remaining_gallons_pair = CityAndRemainingGas(0, 0)
    num_cities = len(gallons)
    for i in range(1, num_cities):
        remaining_gallons += gallons[i - 1] - distances[i - 1] // MPG
        if remaining_gallons < city_remaining_gallons_pair.remaining_gallons:
            city_remaining_gallons_pair = CityAndRemainingGas(
                i, remaining_gallons)
    return city_remaining_gallons_pair.city


@enable_executor_hook
def find_ample_city_wrapper(executor, gallons, distances):
    result = executor.run(
        functools.partial(find_ample_city, gallons, distances))
    num_cities = len(gallons)
    tank = 0
    for i in range(num_cities):
        city = (result + i) % num_cities
        tank += gallons[city] * MPG - distances[city]
        if tank < 0:
            raise TestFailure('Out of gas on city {}'.format(i))


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('refueling_schedule.py',
                                       'refueling_schedule.tsv',
                                       find_ample_city_wrapper))
