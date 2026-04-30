from test_framework import generic_test


def has_two_sum(nums: list[int], target: int) -> bool:
    """
    #17.0

    Time complexity = O(n), where n is the length of the array.
    Space complexity = O(1)

    Test PASSED (1005/1005) [   1 ms]
    Average running time:   36 us
    Median running time:     5 us
    """
    left, right = 0, len(nums) - 1
    while left <= right:
        curr_sum = nums[left] + nums[right]
        if curr_sum == target:
            return True
        if curr_sum < target:
            left += 1
        else:  # target < curr_sum
            right -= 1
    return False


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('two_sum.py', 'two_sum.tsv',
                                       has_two_sum))
