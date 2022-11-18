from test_framework import generic_test


def count_bits(x: int) -> int:
    """
    # 4.0

    Time complexity = O(k), k = # of bits set to 1 in x
    Space complexity = O(1)

    Similar to Leetcode # 191. Number of 1 Bits

    Test PASSED (10001/10001) [  <1 us]
    Average running time:    1 us
    Median running time:     1 us
    """
    num_bits = 0
    while x:
        x &= (x - 1)
        num_bits += 1
    return num_bits


def count_bits_pythonic(x: int) -> int:
    """
    Time complexity = O(n), n = # of bits needed to represent x
    Space complexity = O(1)

    Test PASSED (10001/10001) [  <1 us]
    Average running time:   <1 us
    Median running time:    <1 us
    """
    return bin(x).count('1')


def count_bits_slower(x: int) -> int:
    """
    Time complexity = O(n), n = # of bits needed to represent x
    Space complexity = O(1)

    Test PASSED (10001/10001) [   1 us]
    Average running time:    2 us
    Median running time:     2 us
    """
    num_bits = 0
    while x:
        num_bits += x & 1
        x >>= 1
    return num_bits


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('count_bits.py', 'count_bits.tsv',
                                       count_bits))
