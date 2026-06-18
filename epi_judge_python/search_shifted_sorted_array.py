from test_framework import generic_test


def search_smallest(nums: list[int]) -> int:
    """
    #11.3

    Time complexity  = O(log n)
    Space complexity = O(1)

    Note that this problem cannot, in general, be solved in less than linear
    time when elements may be repeated.
    For example, if A consists of n - 1 1s and a single 0, that 0 cannot be
    detected in the worst-case without inspecting every element.

    Test PASSED (307/307) [   5 us]
    Average running time:   <1 us
    Median running time:    <1 us
    """
    # All elements are distinct.
    if nums[0] <= nums[-1]:  # Not rotated
        return 0
    left, right, result = 0, len(nums) - 1, len(nums) - 1
    while left <= right:
        mid = left + ((right - left) >> 1)
        if nums[mid] < nums[result]:
            result = mid
            right = mid - 1
        else:  # A[result] <= A[mid]
            left = mid + 1
    return result


def search_smallest_faster(nums: list[int]) -> int:
    """
    # TODO: Yet to be fully understood!

    Test PASSED (307/307) [   3 us]
    Average running time:   <1 us
    Median running time:    <1 us
    """
    left, right = 0, len(nums) - 1
    while left < right:
        mid = (left + right) // 2
        if nums[mid] > nums[right]:
            # Minimum must be in A[mid + 1:right + 1].
            left = mid + 1
        else:  # A[mid] <= A[right].
            # Minimum cannot be in A[mid + 1:right + 1] so it must be in
            # A[left:mid + 1].
            right = mid
    # Loop ends when left == right.
    return left


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('search_shifted_sorted_array.py',
                                       'search_shifted_sorted_array.tsv',
                                       search_smallest_faster))
