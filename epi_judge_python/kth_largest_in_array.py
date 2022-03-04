import heapq
import operator
import random
from typing import List

from test_framework import generic_test


# The numbering starts from one, i.e., if A = [3, 1, -1, 2]
# find_kth_largest(1, A) returns 3, find_kth_largest(2, A) returns 2,
# find_kth_largest(3, A) returns 1, and find_kth_largest(4, A) returns -1.
def find_kth_largest(k: int, A: List[int]) -> int:
    """
    Time complexity  = O(n)
    Space complexity = O(1)

    Since we expect to reduce the number of elements to process by roughly half, the average time complexity T(n)
    satisfies T(n) = O(n) + T(n/2). This solves to T(n) = O(n).The space complexity is O(1). The worst-case time
    complexity is O(n**2), which occurs when the randomly selected pivot is the smallest or largest element in the
    current sub-array. The probability of the worst-case reduces exponentially with the length of the input array, and
    the worst-case is a nonissue in practice. For this reason, the randomize selection algorithm is sometimes said to
    have almost certain O(n) time complexity.

    Test PASSED (503/503) [  14 ms]
    Average running time:  105 us
    Median running time:    19 us
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

        def partition_around_pivot(left: int, right: int, pivot_idx: int) -> int:

            pivot_value = A[pivot_idx]
            new_pivot_idx = left
            A[right], A[pivot_idx] = A[pivot_idx], A[right]
            for i in range(left, right):
                if comp(A[i], pivot_value):
                    A[i], A[new_pivot_idx] = A[new_pivot_idx], A[i]
                    new_pivot_idx += 1
            A[right], A[new_pivot_idx] = A[new_pivot_idx], A[right]
            return new_pivot_idx

        left, right = 0, len(A) - 1
        while left <= right:
            # Generates a random integer in [left, right].
            pivot_idx = random.randint(left, right)
            new_pivot_idx = partition_around_pivot(left, right, pivot_idx)
            if new_pivot_idx == k - 1:
                return A[new_pivot_idx]
            elif new_pivot_idx < k - 1:
                left = new_pivot_idx + 1
            else:  # k - 1 < new_pivot_idx
                right = new_pivot_idx - 1

        raise IndexError('no k-th node in array A')

    return find_kth(operator.gt)


def find_kth_largest_pythonic(k: int, A: List[int]) -> int:
    """
    Time complexity  = O(n log n)
    Space complexity = O(n)

    Test PASSED (503/503) [   9 ms]
    Average running time:  102 us
    Median running time:    10 us
    """
    return heapq.nlargest(k, A)[k - 1]


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('kth_largest_in_array.py',
                                       'kth_largest_in_array.tsv',
                                       find_kth_largest))
