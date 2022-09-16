import math
from typing import List

from test_framework import generic_test, test_utils


def generate_power_set_pythonic(input_set: List[int]) -> List[List[int]]:
    """
    #15.4

    Time complexity = O(n * (2 ** n)), where n is the length of input_set.
    Space complexity = O(n * (2 ** n))

    Test PASSED (15/15) [   2 ms]
    Average running time:  340 us
    Median running time:    13 us
    """
    power_set = [[]]
    for i in input_set:
        power_set += [item + [i] for item in power_set]
    return power_set


def generate_power_set(input_set: List[int]) -> List[List[int]]:
    """
    Recursive solution

    Time complexity = O(n * (2 ** n)), where n is the length of input_set.
    Space complexity = O(n * (2 ** n))

    The number of recursive calls, C(n) satisfies the recurrence C(n) = 2C(n - 1), which solves to C(n) = O(2 ** n).
    Since we spend O(n) time within a call, the time complexity is O(n * (2 ** n)).
    The space complexity is O(n * (2 ** n)), since there are 2 ** n subsets, and the average subset size is n / 2.

    Test PASSED (15/15) [   8 ms]
    Average running time:    1 ms
    Median running time:    56 us
    """
    # Generate all subsets whose intersection with input_set[0], ...,
    # input_set[to_be_selected - 1] is exactly selected_so_far.
    def directed_power_set(to_be_selected, selected_so_far):
        if to_be_selected == len(input_set):
            power_set.append(selected_so_far)
            return

        directed_power_set(to_be_selected + 1, selected_so_far)
        # Generate all subsets that contain input_set[to_be_selected].
        directed_power_set(to_be_selected + 1,
                           selected_so_far + [input_set[to_be_selected]])

    power_set: List[List[int]] = []
    directed_power_set(0, [])
    return power_set


def generate_power_set_iterative(input_set: List[int]) -> List[List[int]]:
    """
    Time complexity = O(n * (2 ** n)), where n is the length of input_set.
    Space complexity = O(n * (2 ** n))

    Since each set takes O(n) time to compute, the time complexity is O(n * (2 ** n)).
    In practice, this approach is very fast. Furthermore, its space complexity is O(n) when we want to just enumerate
    subsets, e.g., to print them, rather that to return all the subsets.

    Test PASSED (15/15) [  42 ms]
    Average running time:    5 ms
    Median running time:   158 us
    """
    power_set: List[List[int]] = []
    for int_for_subset in range(1 << len(input_set)):
        bit_array = int_for_subset
        subset = []
        while bit_array:
            subset.append(input_set[int(math.log2(bit_array & ~(bit_array - 1)))])
            bit_array &= (bit_array - 1)
        power_set.append(subset)
    return power_set


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('power_set.py', 'power_set.tsv',
                                       generate_power_set,
                                       test_utils.unordered_compare))
