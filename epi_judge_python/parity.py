from test_framework import generic_test


def parity1(x: int) -> int:
    """The time complexity is O(n), where n is the word size."""
    result = 0
    while x:
        result ^= x & 1
        x >>= 1
    return result


def parity2(x: int) -> int:
    """The time complexity is O(k), where k is the number of bits set to 1 in the word."""
    result = 0
    while x:
        result ^= 1
        x &= x - 1
    return result


def parity3(x: int) -> int:
    """
    The time complexity is a function of the size of the keys used to index the lookup table. Let L be the width of the
    words for which we cache the results, and n the word size. Since there are n=L terms, the time complexity is O(n=L),
    assuming word-level operations, such as shifting, take O(1) time. (This does not include the time for initialization
    of the lookup table.)
    """
    MASK_SIZE = 16
    BIT_MASK = 0xFFFF
    PRECOMPUTED_PARITY = []  # lookup table for 16-bit words
    return (PRECOMPUTED_PARITY[x >> (3 * MASK_SIZE)] ^
            PRECOMPUTED_PARITY[(x >> (2 * MASK_SIZE)) & BIT_MASK] ^
            PRECOMPUTED_PARITY[(x >> MASK_SIZE) & BIT_MASK] ^
            PRECOMPUTED_PARITY[x & BIT_MASK])


def parity(x: int) -> int:
    """The time complexity is O(log n), where n is the word size."""
    x ^= x >> 32
    x ^= x >> 16
    x ^= x >> 8
    x ^= x >> 4
    x ^= x >> 2
    x ^= x >> 1
    return x & 0x1


if __name__ == '__main__':
    exit(generic_test.generic_test_main('parity.py', 'parity.tsv', parity))
