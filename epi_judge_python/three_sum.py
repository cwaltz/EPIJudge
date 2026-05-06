from test_framework import generic_test

"""
In Production: The Outer Function wins decisively. The lack of isolated 
testability and the minor performance hit of redefining the function object on 
every call make inner functions highly undesirable for non-trivial logic in 
enterprise environments.

In a real codebase, the ideal structure would look like this:
"""


def _has_two_sum(nums: list[int], left: int, right: int, target: int) -> bool:
    """
    Private helper to find if two numbers in a sorted array sum to a target.
    """
    while left <= right:
        total = nums[left] + nums[right]
        if total == target:
            return True
        if total < target:
            left += 1
        else:
            right -= 1
    return False


def has_three_sum_production(nums: list[int], target: int) -> bool:
    """
    #17.4

    Time complexity = O(n ** 2), where n is the length of the array.
    Space complexity = O(1)

    Test PASSED (1008/1008) [   1  s]
    Average running time:    1 ms
    Median running time:     6 us
    """
    nums.sort()
    length = len(nums)

    for idx, num in enumerate(nums):
        if _has_two_sum(nums, idx, length - 1, target - num):
            return True

    return False


"""
Production level solution ends.

In an Interview:
Using an inner function is perfectly acceptable and sometimes even preferred. 
It shows the interviewer you understand variable scope and closures in Python, 
and it saves you precious time by keeping your function signatures short on a 
whiteboard or in a shared coder pad.
"""


def has_three_sum_interview(nums: list[int], target: int) -> bool:
    """
    Test PASSED (1008/1008) [   1  s]
    Average running time:    2 ms
    Median running time:     7 us
    """
    nums.sort()
    length = len(nums)

    def has_two_sum_inner(left: int, right: int, sub_target: int) -> bool:
        while left <= right:
            total = nums[left] + nums[right]
            if total == sub_target:
                return True
            if total < sub_target:
                left += 1
            else:  # if sub_target < total:
                right -= 1

        return False

    for idx, num in enumerate(nums):
        if has_two_sum_inner(idx, length - 1, target - num):
            return True

    return False


"""
Interview level solution ends.
"""


def has_three_sum_shorter(nums: list[int], target: int) -> bool:
    """
    Test PASSED (1008/1008) [   1  s]
    Average running time:    1 ms
    Median running time:     7 us
    """
    nums.sort()
    length = len(nums)
    return any(_has_two_sum(nums, idx, length - 1, target - num)
               for idx, num in enumerate(nums))


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('three_sum.py', 'three_sum.tsv',
                                       has_three_sum_shorter))
