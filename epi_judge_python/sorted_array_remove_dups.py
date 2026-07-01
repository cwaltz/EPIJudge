import functools

from test_framework import generic_test
from test_framework.test_utils import enable_executor_hook


def delete_duplicates(nums: list[int]) -> int:
    """
    #5.5

    Time complexity  = O(n), where n = length of nums
    Space complexity = O(1)

    Test PASSED (2003/2003) [   4 ms]
    Average running time:    9 us
    Median running time:     2 us
    """
    if not nums:
        return 0

    length = len(nums)
    write_idx = 0
    for read_idx in range(1, length):
        if nums[read_idx] != nums[write_idx]:
            write_idx += 1
            nums[write_idx] = nums[read_idx]

    return write_idx + 1


def delete_duplicates_1(nums: list[int]) -> int:
    """
    Time complexity  = O(n), where n = length of nums
    Space complexity = O(1)

    Test PASSED (2003/2003) [   2 ms]
    Average running time:    7 us
    Median running time:     2 us
    """
    if not nums:
        return 0

    write_idx = 0
    prev_num = nums[0] - 1  # Could cause an integer underflow
    # Would throw TypeError for types other than int/float
    for num in nums:
        if num != prev_num:
            nums[write_idx] = prev_num = num
            # The above chained Assignment hurts readability. It forces the
            # reader to pause and parse the execution order (right-to-left).
            write_idx += 1

    return write_idx


def delete_duplicates_2(nums: list[int]) -> int:
    """
    Time complexity  = O(n), where n = length of nums
    Space complexity = O(n)

    Test PASSED (2003/2003) [   1 ms]
    Average running time:    5 us
    Median running time:     3 us
    """
    if not nums:
        return 0

    nums_set = set(nums)
    length = len(nums_set)
    nums[:length] = sorted(nums_set)
    return length


def delete_duplicates_3(nums: list[int]) -> int:
    """
    Time complexity  = O(n), where n = length of nums
    Space complexity = O(n)

    Test PASSED (2003/2003) [   1 ms]
    Average running time:    5 us
    Median running time:     2 us
    """
    if not nums:
        return 0

    nums_dict = dict.fromkeys(nums)
    length = len(nums_dict)
    nums[:length] = list(nums_dict)
    return length


@enable_executor_hook
def delete_duplicates_wrapper(executor, nums):
    idx = executor.run(functools.partial(delete_duplicates_3, nums))
    return nums[:idx]


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('sorted_array_remove_dups.py',
                                       'sorted_array_remove_dups.tsv',
                                       delete_duplicates_wrapper))
