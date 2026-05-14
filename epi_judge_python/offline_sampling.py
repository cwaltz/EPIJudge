import functools
from random import randint, sample

from test_framework import generic_test
from test_framework.random_sequence_checker import (
    binomial_coefficient, check_sequence_is_uniformly_random,
    compute_combination_idx, run_func_with_retries)
from test_framework.test_utils import enable_executor_hook


def random_sampling(k: int, nums: list[int]) -> None:
    """
    #5.12

    Time complexity = O(min(k, n - k)) to select the elements.
    Space complexity = O(1)

    The algorithm makes min(k, n - k) calls to the random number generator.
    When k is bigger than n / 2, we optimize by computing a subset of n - k
    elements to remove from the set. For example, when k = n - 1,
    this replaces n - 1 calls to the random number generator with a single call.

    Test PASSED (8/8) [  98 ms]
    Average running time:   71 ms
    Median running time:    69 ms
    """
    n = len(nums)
    if k <= n // 2:
        for i in range(k):
            # Generate a random index r in [i, len(A) - 1]. A[r] is included
            # in the subset.
            r = randint(i, n - 1)
            nums[i], nums[r] = nums[r], nums[i]
    else:
        for i in range(n - 1, k - 1, -1):
            # Generate a random index r in [0, i]. A[r] is excluded from the
            # subset.
            r = randint(0, i)
            nums[i], nums[r] = nums[r], nums[i]


# Pythonic solution
def random_sampling_pythonic(k: int, nums: list[int]) -> None:
    """
    Test PASSED (8/8) [ 147 ms]
    Average running time:  145 ms
    Median running time:   147 ms
    """
    nums[:] = sample(nums, k)


@enable_executor_hook
def random_sampling_wrapper(executor, k, nums):
    def random_sampling_runner(executor, k, nums):
        result = []

        def populate_random_sampling_result():
            for _ in range(100000):
                random_sampling(k, nums)
                result.append(nums[:k])

        executor.run(populate_random_sampling_result)

        total_possible_outcomes = binomial_coefficient(len(nums), k)
        nums = sorted(nums)
        comb_to_idx = {
            tuple(compute_combination_idx(nums, len(nums), k, i)): i
            for i in range(binomial_coefficient(len(nums), k))
        }

        return check_sequence_is_uniformly_random(
            [comb_to_idx[tuple(sorted(a))] for a in result],
            total_possible_outcomes, 0.01)

    run_func_with_retries(
        functools.partial(random_sampling_runner, executor, k, nums))


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('offline_sampling.py',
                                       'offline_sampling.tsv',
                                       random_sampling_wrapper))
