from test_framework import generic_test


"""
The actual runtimes depend on the input data, e.g., the refinement (parity3) of the brute-force algorithm (parity4) is
very fast on sparse inputs. However, for random inputs, the refinement of the brute-force is roughly 20% faster than the
brute-force algorithm. The table-based approach (parity1) is four times faster still, and using associativity (parity)
reduces run time by another factor of two.
"""


def parity(x: int) -> int:
    """
    The time complexity is O(log n), where n is the word size.

    Test PASSED (10000/10000) [   1 us]
    Average running time:    1 us
    Median running time:     1 us
    """
    x ^= x >> 32
    x ^= x >> 16
    x ^= x >> 8
    x ^= x >> 4
    x ^= x >> 2
    x ^= x >> 1
    return x & 0x1


def parity1(x: int) -> int:
    """
    The time complexity is a function of the size of the keys used to index the lookup table. Let L (= 16 here) be the
    width of the words for which we cache the results, and n (= 64 here) the word size. Since there are n / L (= 4 here)
    terms, the time complexity is O(n / L), assuming word-level operations, such as shifting, take O(1) time. (This does
    not include the time for initialization of the lookup table.)
    """
    MASK_SIZE = 16
    BIT_MASK = 0xFFFF
    PRECOMPUTED_PARITY = []  # lookup table for 16-bit words
    return (PRECOMPUTED_PARITY[x >> (3 * MASK_SIZE)] ^
            PRECOMPUTED_PARITY[(x >> (2 * MASK_SIZE)) & BIT_MASK] ^
            PRECOMPUTED_PARITY[(x >> MASK_SIZE) & BIT_MASK] ^
            PRECOMPUTED_PARITY[x & BIT_MASK])


def parity2(x: int) -> int:
    """
    The time complexity is O(k), where k is the number of bits set to 1 in the word.

    Test PASSED (10000/10000) [   3 us]
    Average running time:    4 us
    Median running time:     3 us
    """
    result = 0
    while x:
        result ^= 1
        x &= x - 1  # Drops the lowest set bit of x.
    return result


def parity3(x: int) -> int:
    """
    The time complexity is O(n), where n is the word size.

    Test PASSED (10000/10000) [   9 us]
    Average running time:    6 us
    Median running time:     6 us
    """
    result = 0
    while x:
        result ^= x & 1
        x >>= 1
    return result


if __name__ == '__main__':
    exit(generic_test.generic_test_main('parity.py', 'parity.tsv', parity))
