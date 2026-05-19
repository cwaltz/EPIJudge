from heapq import nlargest, nsmallest
from operator import gt, lt
from random import randint

from test_framework import generic_test


# The numbering starts from one, i.e., if A = [3, 1, -1, 2]
# find_kth_largest(1, A) returns 3, find_kth_largest(2, A) returns 2,
# find_kth_largest(3, A) returns 1, and find_kth_largest(4, A) returns -1.
def find_kth_largest(k: int, nums: list[int]) -> int:
    """
    #11.8

    Time complexity = O(n) on average. O(n ** 2) in the worst case.
    Space complexity = O(1)

    All elements are distinct.

    Since we expect to reduce the number of elements to process by roughly
    half, the average time complexity T(n) satisfies T(n) = O(n) + T(n/2).
    This solves to T(n) = O(n).The space complexity is O(1). The worst-case
    time complexity is O(n ** 2), which occurs when the randomly selected
    pivot is the smallest or largest element in the current sub-array. The
    probability of the worst-case reduces exponentially with the length of
    the input array, and the worst-case is a nonissue in practice. For this
    reason, the 'randomize' selection algorithm is sometimes said to have
    almost certain O(n) time complexity.

    Test PASSED (503/503) [  11 ms]
    Average running time:   91 us
    Median running time:    16 us
    """

    def find_kth(comp):
        # Partition A[left:right + 1] around pivot_idx, returns the new index of
        # the pivot, new_pivot_idx, after partition. After partitioning,
        # A[left:new_pivot_idx] contains elements that are "greater than" the
        # pivot, and A[new_pivot_idx + 1:right + 1] contains elements that are
        # "less than" the pivot.
        #
        # Note: "greater than" and "less than" are defined by the comp object.
        #
        # Returns the new index of the pivot element after partition.

        def partition_around_pivot(
                left: int, right: int, pivot_idx: int) -> int:

            pivot_value = nums[pivot_idx]
            new_pivot_idx = left
            nums[right], nums[pivot_idx] = nums[pivot_idx], nums[right]
            for i in range(left, right):
                if comp(nums[i], pivot_value):
                    nums[i], nums[new_pivot_idx] = nums[new_pivot_idx], nums[i]
                    new_pivot_idx += 1
            nums[right], nums[new_pivot_idx] = nums[new_pivot_idx], nums[right]
            return new_pivot_idx

        left, right = 0, len(nums) - 1
        while left <= right:
            # Generates a random integer in [left, right].
            pivot_idx = randint(left, right)
            new_pivot_idx = partition_around_pivot(left, right, pivot_idx)
            if new_pivot_idx == k - 1:
                return nums[new_pivot_idx]
            elif new_pivot_idx < k - 1:
                left = new_pivot_idx + 1
            else:  # k - 1 < new_pivot_idx
                right = new_pivot_idx - 1

        raise IndexError('no k-th node in array A')

    return find_kth(gt)


# The numbering starts from one, i.e., if A = [3, 1, -1, 2] then
# find_kth_smallest(1, A) returns -1, find_kth_smallest(2, A) returns 1,
# find_kth_smallest(3, A) returns 2, and find_kth_smallest(4, A) returns 3.
def find_kth_smallest(k, nums):
    def find_kth(comp):
        # Partition A[left:right + 1] around pivot_idx, returns the new index of
        # the pivot, new_pivot_idx, after partition. After partitioning,
        # A[left:new_pivot_idx] contains elements that are "greater than" the
        # pivot, and A[new_pivot_idx + 1:right + 1] contains elements that are
        # "less than" the pivot.
        #
        # Note: "greater than" and "less than" are defined by the comp object.
        #
        # Returns the new index of the pivot element after partition.
        def partition_around_pivot(left, right, pivot_idx):
            pivot_value = nums[pivot_idx]
            new_pivot_idx = left
            nums[pivot_idx], nums[right] = nums[right], nums[pivot_idx]
            for i in range(left, right):
                if comp(nums[i], pivot_value):
                    nums[i], nums[new_pivot_idx] = nums[new_pivot_idx], nums[i]
                    new_pivot_idx += 1
            nums[right], nums[new_pivot_idx] = nums[new_pivot_idx], nums[right]
            return new_pivot_idx

        left, right = 0, len(nums) - 1
        while left <= right:
            # Generates a random integer in [left, right].
            pivot_idx = randint(left, right)
            new_pivot_idx = partition_around_pivot(left, right, pivot_idx)
            if new_pivot_idx == k - 1:
                return nums[new_pivot_idx]
            elif new_pivot_idx > k - 1:
                right = new_pivot_idx - 1
            else:  # new_pivot_idx < k - 1.
                left = new_pivot_idx + 1
        raise IndexError('no k-th node in array A')

    return find_kth(lt)


def find_kth_largest_pythonic(k: int, nums: list[int]) -> int:
    """
    Time complexity = O(n log n)
    Space complexity = O(n)

    Test PASSED (503/503) [   9 ms]
    Average running time:  102 us
    Median running time:    10 us
    """
    return nlargest(k, nums)[k - 1]


def find_kth_smallest_pythonic(k: int, nums: list[int]) -> int:
    """
    Time complexity = O(n log n)
    Space complexity = O(n)
    """
    return nsmallest(k, nums)[k - 1]


def find_kth_largest_using_sort(k: int, nums: list[int]) -> int:
    """
    Time complexity = O(n log n)
    Space complexity = O(n)

    Test PASSED (503/503) [ 207 us]
    Average running time:   23 us
    Median running time:     2 us
    """
    nums.sort()
    return nums[-k]


def find_kth_smallest_using_sort(k: int, nums: list[int]) -> int:
    """
    Time complexity = O(n log n)
    Space complexity = O(n)
    """
    nums.sort()
    return nums[k - 1]


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('kth_largest_in_array.py',
                                       'kth_largest_in_array.tsv',
                                       find_kth_largest_using_sort))
