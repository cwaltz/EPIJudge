import itertools
from typing import List

from next_permutation import next_permutation
from test_framework import generic_test, test_utils


def permutations1(nums: List[int]) -> List[List[int]]:
    """
    #15.3

    Time complexity = O(n * n!), where n is the length of nums.
    Space complexity = O(n * n!)

    The time complexity is determined by the number of recursive calls, since
    within each function the time spent is O(1), not including the time in the
    sub calls. The number of function calls, C(n) satisfies the recurrence
    C(n) = 1 + nC(n - 1) for n >= 1, with C(0) = 1. Expanding this, we see
    C(n) = 1 + n + n(n - 1) + n(n - 1)(n - 2) + ... + n!
    = n!(1 / n! + 1 / (n - 1)! + 1 / (n - 2)! + ... + 1 / 1!).
    The sum (1 + 1/1! + 1/2! + ... + 1/n!) tends to Euler's number e,
    so C(n) tends to (e - 1)n!, i.e., O(n!). The time complexity T(n) is
    O(n * n!), since we do O(n) computation per call outside the recursive calls

    Test PASSED (8/8) [  31 ms]
    Average running time:    4 ms
    Median running time:    51 us
    """
    def directed_permutations(i):
        if i == n - 1:
            result.append(nums.copy())
            return

        # Try every possibility for nums[i].
        for j in range(i, n):
            nums[i], nums[j] = nums[j], nums[i]
            # Generate all permutations for nums[i + 1:].
            directed_permutations(i + 1)
            nums[i], nums[j] = nums[j], nums[i]

    result: List[List[int]] = []
    n = len(nums)
    directed_permutations(0)
    return result


def permutations_iterative(nums: List[int]) -> List[List[int]]:
    """
    Time complexity = O(n * n!), where n is the length of nums.
    Space complexity = O(n * n!)

    Test PASSED (8/8) [  51 ms]
    Average running time:    7 ms
    Median running time:    93 us
    """
    result: List[List[int]] = []
    nums.sort()
    while True:
        result.append(nums.copy())
        nums = next_permutation(nums)
        if not nums:
            break
    return result


def permutations(nums: List[int]) -> List[List[int]]:
    """
    Test PASSED (8/8) [  19 ms]
    Average running time:    2 ms
    Median running time:    21 us
    """
    # return list(map(list, set(itertools.permutations(nums))))
    """
    Test PASSED (8/8) [  13 ms]
    Average running time:    1 ms
    Median running time:    14 us
    """
    return list(map(list, list(itertools.permutations(nums))))


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('permutations.py', 'permutations.tsv',
                                       permutations,
                                       test_utils.unordered_compare))
