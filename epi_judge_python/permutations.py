import itertools

from next_permutation import next_permutation
from test_framework import generic_test, test_utils


def permutations(nums: list[int]) -> list[list[int]]:
    """
    #15.3

    Time complexity = O(n * n!), where n is the n of nums.
    Space complexity = O(n * n!)

    The time complexity is determined by the number of recursive calls, since
    within each function the time spent is O(1), not including the time in the
    sub calls. The number of function calls, C(n) satisfies the recurrence
    C(n) = 1 + nC(n - 1) for n >= 1, with C(0) = 1.

    Expanding this, we see
    C(n) = 1 + n + n(n - 1) + n(n - 1)(n - 2) + ... + n!
         = n!(1 / n! + 1/ (n - 1)! + 1 / (n - 2)! + ... + 1 / 1!).

    The sum (1 + 1/1! + 1/2! + ... + 1/n!) tends to Euler's number e,
    so C(n) tends to (e - 1)n!, i.e., O(n!).

    The time complexity T(n) is O(n * n!),
    since we do O(n) computation per call outside the recursive calls.

    Test PASSED (8/8) [  23 ms]
    Average running time:    3 ms
    Median running time:    41 us
    """
    length = len(nums)
    if length < 2:
        return [nums]

    def directed_permutations(next_idx: int) -> None:
        if next_idx == length - 1:
            result.append(nums.copy())
            return

        # Try every possibility for nums[i].
        for i in range(next_idx, length):
            nums[next_idx], nums[i] = nums[i], nums[next_idx]
            # Generate all permutations for nums[i + 1:].
            directed_permutations(next_idx + 1)
            nums[next_idx], nums[i] = nums[i], nums[next_idx]

    result: list[list[int]] = []
    directed_permutations(0)
    return result


def permutations_iterative(nums: list[int]) -> list[list[int]]:
    """
    Time complexity = O(n * n!), where n is the length of nums.
    Space complexity = O(n * n!)

    Test PASSED (8/8) [  51 ms]
    Average running time:    7 ms
    Median running time:    93 us
    """
    result: list[list[int]] = []
    nums.sort()
    while True:
        result.append(nums.copy())
        nums = next_permutation(nums)  # TODO: To be implemented
        if not nums:
            break
    return result


def permutations_using_itertools(nums: list[int]) -> list[list[int]]:
    """
    Test PASSED (8/8) [   5 ms]
    Average running time:  834 us
    Median running time:    11 us
    """
    return list(map(list, list(itertools.permutations(nums))))

    """
    Test PASSED (8/8) [   9 ms]
    Average running time:    1 ms
    Median running time:    12 us
    """
    # return [list(y) for y in list(itertools.permutations(nums))]

    """
    Test PASSED (8/8) [  10 ms]
    Average running time:    1 ms
    Median running time:    17 us
    """
    # return list(map(list, set(itertools.permutations(nums))))


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('permutations.py', 'permutations.tsv',
                                       permutations_using_itertools,
                                       test_utils.unordered_compare))
