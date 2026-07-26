from test_framework import generic_test


MASK_SIZE = 16
BIT_MASK = 0xFFFF
CACHE = [int(f"{i:016b}"[::-1], 2) for i in range(1 << 16)]


def reverse_bits(num: int) -> int:
    """
    #4.3

    Time complexity  = O(n), where n is number of bits needed to represent y.
    Space complexity = O(1)

    Test PASSED (10000/10000) [   2 us]
    Average running time:    1 us
    Median running time:     1 us
    """
    return (CACHE[num & BIT_MASK] << (MASK_SIZE * 3) |
            CACHE[(num >> MASK_SIZE) & BIT_MASK] << (MASK_SIZE * 2) |
            CACHE[(num >> (MASK_SIZE * 2)) & BIT_MASK] << (MASK_SIZE * 1) |
            CACHE[(num >> (MASK_SIZE * 3)) & BIT_MASK])


"""
MASK_SIZE = 2
BIT_MASK = 3  # 0x3
PRECOMPUTED_REVERSE = [0, 2, 1, 3]
# [int(f"{i:02b}"[::-1], 2) for i in range(1 << 2)]

Test PASSED (10000/10000) [   6 us]
Average running time:    6 us
Median running time:     6 us
"""
"""
MASK_SIZE = 4
BIT_MASK = 0xF
PRECOMPUTED_REVERSE = [0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15]
# [int(f"{i:04b}"[::-1], 2) for i in range(1 << 4)]

Test PASSED (10000/10000) [   3 us]
Average running time:    3 us
Median running time:     3 us
"""
MASK_SIZE_1 = 8
BIT_MASK_1 = 0xFF
PRECOMPUTED_REVERSE = [0, 128, 64, 192, 32, 160, 96, 224, 16, 144, 80, 208, 48,
                       176, 112, 240, 8, 136, 72, 200, 40, 168, 104, 232, 24,
                       152, 88, 216, 56, 184, 120, 248, 4, 132, 68, 196, 36,
                       164, 100, 228, 20, 148, 84, 212, 52, 180, 116, 244, 12,
                       140, 76, 204, 44, 172, 108, 236, 28, 156, 92, 220, 60,
                       188, 124, 252, 2, 130, 66, 194, 34, 162, 98, 226, 18,
                       146, 82, 210, 50, 178, 114, 242, 10, 138, 74, 202, 42,
                       170, 106, 234, 26, 154, 90, 218, 58, 186, 122, 250, 6,
                       134, 70, 198, 38, 166, 102, 230, 22, 150, 86, 214, 54,
                       182, 118, 246, 14, 142, 78, 206, 46, 174, 110, 238, 30,
                       158, 94, 222, 62, 190, 126, 254, 1, 129, 65, 193, 33,
                       161, 97, 225, 17, 145, 81, 209, 49, 177, 113, 241, 9,
                       137, 73, 201, 41, 169, 105, 233, 25, 153, 89, 217, 57,
                       185, 121, 249, 5, 133, 69, 197, 37, 165, 101, 229, 21,
                       149, 85, 213, 53, 181, 117, 245, 13, 141, 77, 205, 45,
                       173, 109, 237, 29, 157, 93, 221, 61, 189, 125, 253, 3,
                       131, 67, 195, 35, 163, 99, 227, 19, 147, 83, 211, 51,
                       179, 115, 243, 11, 139, 75, 203, 43, 171, 107, 235, 27,
                       155, 91, 219, 59, 187, 123, 251, 7, 135, 71, 199, 39,
                       167, 103, 231, 23, 151, 87, 215, 55, 183, 119, 247, 15,
                       143, 79, 207, 47, 175, 111, 239, 31, 159, 95, 223, 63,
                       191, 127, 255]
SIZE = 64


def reverse_bits_extensible(num: int) -> int:
    """
    Test PASSED (10000/10000) [   1 us]
    Average running time:    2 us
    Median running time:     2 us
    """
    result = 0
    for i in range(SIZE // MASK_SIZE_1):
        bits = (num >> (MASK_SIZE_1 * i)) & BIT_MASK_1
        curr = PRECOMPUTED_REVERSE[bits]
        result = ((result << MASK_SIZE_1) | curr)
    return result


def reverse_bits_pythonic(num: int) -> int:
    """
    Test PASSED (10000/10000) [  <1 us]
    Average running time:   <1 us
    Median running time:    <1 us
    """
    return int(f"{num:064b}"[::-1], 2)


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('reverse_bits.py', 'reverse_bits.tsv',
                                       reverse_bits))
