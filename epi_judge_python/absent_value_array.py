import itertools
from typing import Iterator

from test_framework import generic_test
from test_framework.test_failure import TestFailure


def find_missing_element(stream: Iterator[int]) -> int:
    """
    #11.9

    Time complexity = O(n), where n is the number of elements in the stream (= 2 ** 32 in this case).
    Space complexity = O(2 ** 16)
    The storage requirement is dominated by the count array, i.e., 2 ** 16 integer entries.

    We can count the number of IP addresses in the file that begin with 0,1,2,...,2 ** 16 - 1 using an array of
    2 ** 16 integers that can be represented with 32 bits. For every IP address in the file, we take its 16 MSBs to
    index into this array and increment the count of that number. Since the file contains fewer than 2 ** 32 numbers,
    there must be one entry in the array that is less than 2 ** 16, this tells us that there is at least one IP address
    which has those upper bits and is not in the file. In the second pass, we can focus only on the addresses whose
    leading 16 bits match the one we have found, and use a bit array of size 2 ** 16 to identify a missing address.

    Test PASSED (100/100) [ 657 us]
    Average running time:  670 us
    Median running time:   668 us
    """
    num_bucket = 1 << 16
    counter = [0] * num_bucket
    stream, stream_copy = itertools.tee(stream)
    for x in stream:
        upper_part_x = x >> 16
        counter[upper_part_x] += 1

    # Look for a bucket that contains less than (1 << 16) elements.
    bucket_capacity = 1 << 16
    candidate_bucket = next(i for i, c in enumerate(counter)
                            if c < bucket_capacity)

    # Finds all IP addresses in the stream whose first 16 bits are equal to candidate_bucket.
    candidates = [0] * bucket_capacity
    for x in stream_copy:
        upper_part_x = x >> 16
        if candidate_bucket == upper_part_x:
            # Records the presence of 16 LSB of x.
            lower_part_x = ((1 << 16) - 1) & x
            candidates[lower_part_x] = 1

    # At least one of the LSB combinations is absent, find it.
    for i, v in enumerate(candidates):
        if v == 0:
            return (candidate_bucket << 16) | i

    raise ValueError('no missing element')


def find_missing_element_wrapper(stream):
    try:
        res = find_missing_element(iter(stream))
        if res in stream:
            raise TestFailure('{} appears in stream'.format(res))
    except ValueError:
        raise TestFailure('Unexpected no missing element exception')


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('absent_value_array.py',
                                       'absent_value_array.tsv',
                                       find_missing_element_wrapper))
