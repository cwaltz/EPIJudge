"""
#11.10

This problem does not really test data structures or algorithms. Its focus is
more on maths and bit manipulation. If you are in a hurry, skip the O(1) space
approaches.

This problem is difficult or easy depending on the tools that we are allowed to
use.

A straightforward & intuitive approach is to use a counter
(collections.Counter or a dictionary):
find_duplicate_missing_using_counter() takes O(n) time, O(n) space.

Another intuitive approach is to use sorting:
find_duplicate_missing_using_sorting() takes O(n log n) time, O(n) space.

The following approaches satisfy the O(1) space requirement:

A purely mathematical approach can be implemented:
find_duplicate_missing_using_math() takes O(n) time, O(1) space.

Maths & Bit Magic approach provided by EPI and improved by Gemini:
TODO: To be understood
find_duplicate_missing_gemini() takes O(n) time, O(1) space.

Maths & Bit Magic approach provided by EPI:
TODO: Skip it & focus on the Gemini implementation above
find_duplicate_missing_epi() takes O(n) time, O(1) space.
"""

import collections
import functools
from typing import NamedTuple

from test_framework import generic_test
from test_framework.test_failure import PropertyName


# DuplicateAndMissing = collections.namedtuple('DuplicateAndMissing',
#                                              ('duplicate', 'missing'))
class DuplicateAndMissing(NamedTuple):
    duplicate: int
    missing: int


def find_duplicate_missing_using_counter(
        nums: list[int]) -> DuplicateAndMissing:
    """
    Time complexity = O(n)
    Space complexity = O(n)

    Test PASSED (50/50) [   2 ms]
    Average running time:  301 us
    Median running time:   245 us
    """

    length = len(nums)
    counter = collections.Counter(nums)
    duplicate, missing = -1, -1

    for i in range(length):
        if counter[i] == 0:
            missing = i
        elif counter[i] == 2:
            duplicate = i
        if duplicate != -1 and missing != -1:
            return DuplicateAndMissing(duplicate, missing)

    raise ValueError("Invalid input: Array must contain exactly one duplicate "
                     "and one missing element.")


def find_duplicate_missing_using_sorting(
        nums: list[int]) -> DuplicateAndMissing:
    """
    Time complexity = O(n log n) due to sorting
    Space complexity = O(n) due to sorting

    Test PASSED (50/50) [   4 ms]
    Average running time:  574 us
    Median running time:   453 us
    """

    length = len(nums)
    sorted_nums = sorted(nums)
    duplicate, missing = -1, -1

    # Check boundary edge case: if 0 is missing, it won't be at the start
    if sorted_nums[0] != 0:
        missing = 0

    for i in range(1, length):
        # If two adjacent numbers are the same, we found the duplicate
        if sorted_nums[i] == sorted_nums[i - 1]:
            duplicate = sorted_nums[i]

        # If the gap between adjacent numbers is greater than 1,
        # the missing number is between them
        elif sorted_nums[i] > sorted_nums[i - 1] + 1:
            missing = sorted_nums[i - 1] + 1

        if duplicate != -1 and missing != -1:
            return DuplicateAndMissing(duplicate, missing)

    # Check boundary edge case: if the missing number is the very last expected
    # element
    if missing == -1:
        missing = length - 1

    if duplicate != -1:
        return DuplicateAndMissing(duplicate, missing)

    raise ValueError("Invalid input: Array must contain exactly one duplicate "
                     "and one missing element.")


def find_duplicate_missing_using_math(
        nums: list[int]) -> DuplicateAndMissing:
    """
    Gemini says: "Because Python natively handles arbitrarily large integers,
    you don't even have to worry about the integer overflow risks that would
    plague this solution in C++ or Java."
    Not sure if the integer overflow risk is in python is 0 in practice! :)

    Test PASSED (50/50) [   1 ms]
    Average running time:  164 us
    Median running time:   143 us
    """
    n = len(nums)

    # Calculate the expected sums of indices and their squares
    expected_sum = (n * (n - 1)) // 2
    expected_sum_squares = (n - 1) * n * (2 * n - 1) // 6

    # Calculate the actual sums of the array elements and their squares
    actual_sum = sum(nums)
    actual_sum_squares = sum(val * val for val in nums)

    # diff = missing - duplicate
    diff = expected_sum - actual_sum

    # square_diff = missing^2 - duplicate^2
    square_diff = expected_sum_squares - actual_sum_squares

    # sum_both = missing + duplicate
    #          = (missing^2 - duplicate^2) / (missing - duplicate)
    sum_both = square_diff // diff

    missing = (diff + sum_both) // 2
    duplicate = sum_both - missing

    return DuplicateAndMissing(duplicate, missing)


def find_duplicate_missing_gemini(nums: list[int]) -> DuplicateAndMissing:
    """
    Finds the duplicate and missing elements in an array of size n containing
    elements from 0 to n-1.

    Uses XOR bit-manipulation to achieve O(n) time and O(1) space.

    Test PASSED (50/50) [   4 ms]
    Average running time:  525 us
    Median running time:   456 us
    """
    miss_xor_dup = 0

    # 1. XOR all indices and values.
    # This leaves us with (missing ^ duplicate)
    for i, num in enumerate(nums):
        miss_xor_dup ^= i ^ num

    # 2. Isolate the lowest set bit.
    # This bit is 1 because 'missing' and 'duplicate' differ at this position.
    differ_bit = miss_xor_dup & -miss_xor_dup

    miss_or_dup = 0

    # 3. Partition the numbers into two groups based on the differ_bit.
    # By XORing one group, we isolate either the missing or the duplicate number
    for i, num in enumerate(nums):
        if i & differ_bit:
            miss_or_dup ^= i
        if num & differ_bit:
            miss_or_dup ^= num

    # 4. Identify which is which
    # Note: 'in' is an O(n) operation on a list.
    if miss_or_dup in nums:
        return DuplicateAndMissing(miss_or_dup, miss_or_dup ^ miss_xor_dup)

    return DuplicateAndMissing(miss_or_dup ^ miss_xor_dup, miss_or_dup)


def find_duplicate_missing_epi(nums: list[int]) -> DuplicateAndMissing:
    """
    Test PASSED (50/50) [   6 ms]
    Average running time:  707 us
    Median running time:   620 us
    """

    # Compute the XOR of all numbers from 0 to |A| - 1 and all entries in A.
    miss_xor_dup = functools.reduce(
        lambda v, j: v ^ j[0] ^ j[1], enumerate(nums), 0)

    # We need to find a bit that's set to 1 in miss_xor_dup. Such a bit must
    # exist if there is a single missing number and a single duplicated number
    # in A.
    #
    # The bit-fiddling assignment below sets all bits in differ_bit
    # to 0 except for the least significant bit in miss_xor_dup that's 1.
    differ_bit, miss_or_dup = miss_xor_dup & (~(miss_xor_dup - 1)), 0
    for i, a in enumerate(nums):
        # Focus on entries and numbers in which the differ_bit-th bit is 1.
        if i & differ_bit:
            miss_or_dup ^= i
        if a & differ_bit:
            miss_or_dup ^= a

    # miss_or_dup is either the missing value or the duplicated entry.
    # If miss_or_dup is in A, miss_or_dup is the duplicate;
    # otherwise, miss_or_dup is the missing value.
    return (DuplicateAndMissing(miss_or_dup, miss_or_dup
                                ^ miss_xor_dup) if miss_or_dup in nums else
            DuplicateAndMissing(miss_or_dup ^ miss_xor_dup, miss_or_dup))


def res_printer(prop, value):
    def fmt(x):
        return 'duplicate: {}, missing: {}'.format(x[0], x[1]) if x else None

    return fmt(value) if prop in (PropertyName.EXPECTED,
                                  PropertyName.RESULT) else value


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('search_for_missing_element.py',
                                       'find_missing_and_duplicate.tsv',
                                       find_duplicate_missing_gemini,
                                       res_printer=res_printer))
