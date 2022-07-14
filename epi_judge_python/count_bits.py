from test_framework import generic_test


def count_bits(x: int) -> int:
    """
    Time complexity  = O(k), where k is the number of bits set to 1 in the word.
    Space complexity = O(1)

    Test PASSED (10001/10001) [   2 us]
    Average running time:    2 us
    Median running time:     2 us
    """
    num_bits = 0
    while x:
        x &= (x - 1)
        num_bits += 1
    return num_bits


def count_bits1(x: int) -> int:
    """
    Time complexity  = O(n), since we perform O(1) computation per bit, the time complexity is O(n), where n is the
    number of bits needed to represent the integer.
    Space complexity = O(1)

    Test PASSED (10001/10001) [   3 us]
    Average running time:    4 us
    Median running time:     4 us
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
