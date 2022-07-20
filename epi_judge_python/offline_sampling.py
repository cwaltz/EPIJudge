import functools
import random
from typing import List

from test_framework import generic_test
from test_framework.random_sequence_checker import (
    binomial_coefficient, check_sequence_is_uniformly_random,
    compute_combination_idx, run_func_with_retries)
from test_framework.test_utils import enable_executor_hook


def random_sampling(k: int, A: List[int]) -> None:
    """
    #5.12

    Time complexity = O(min(k, n - k)) to select the elements.
    Space complexity = O(1)

    The algorithm makes min(k, n - k) calls to the random number generator. When k is bigger than n / 2, we optimize by
    computing a subset of n - k elements to remove from the set. For example, when k = n - 1, this replaces n - 1 calls
    to the random number generator with a single call.

    Test PASSED (8/8) [ 243 ms]
    Average running time:  162 ms
    Median running time:   152 ms
    """
    n = len(A)
    if k <= n // 2:
        for i in range(k):
            # Generate a random index r in [i, len(A) - 1]. A[r] is included in the subset.
            r = random.randint(i, n - 1)
            A[i], A[r] = A[r], A[i]
    else:
        for i in range(n - 1, k - 1, -1):
            # Generate a random index r in [0, i]. A[r] is excluded from the subset.
            r = random.randint(0, i)
            A[i], A[r] = A[r], A[i]


# Pythonic solution
def random_sampling_pythonic(k, A):
    """
    Test PASSED (8/8) [ 268 ms]
    Average running time:  269 ms
    Median running time:   268 ms
    """
    A[:] = random.sample(A, k)


@enable_executor_hook
def random_sampling_wrapper(executor, k, A):
    def random_sampling_runner(executor, k, A):
        result = []

        def populate_random_sampling_result():
            for _ in range(100000):
                random_sampling(k, A)
                result.append(A[:k])

        executor.run(populate_random_sampling_result)

        total_possible_outcomes = binomial_coefficient(len(A), k)
        A = sorted(A)
        comb_to_idx = {
            tuple(compute_combination_idx(A, len(A), k, i)): i
            for i in range(binomial_coefficient(len(A), k))
        }

        return check_sequence_is_uniformly_random(
            [comb_to_idx[tuple(sorted(a))] for a in result],
            total_possible_outcomes, 0.01)

    run_func_with_retries(
        functools.partial(random_sampling_runner, executor, k, A))


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('offline_sampling.py',
                                       'offline_sampling.tsv',
                                       random_sampling_wrapper))
