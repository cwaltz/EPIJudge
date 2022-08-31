from typing import List


def binary_search(nums: List[int], target: int) -> int:
    """
    #11.00

    Time complexity = O(log n), where n is the size of nums.
    Space complexity = O(1)
    """
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = left + (right - left) >> 1
        if target < nums[mid]:
            right = mid - 1
        elif target == nums[mid]:
            return mid
        else:  # nums[mid] < target
            left = mid + 1
    return -1
