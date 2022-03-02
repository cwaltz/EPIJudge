from test_framework import generic_test


def square_root(k: int) -> int:
    """
    The time complexity is that of binary search over the interval [0, k], i.e., O(log k)
    Space complexity = O(1)
    """
    left, right, root = 0, k, 0
    while left <= right:
        mid = left + (right - left) // 2
        mid_squared = mid * mid
        if mid_squared == k:
            return mid
        elif mid_squared < k:
            root = mid
            left = mid + 1
        else:  # square < mid_squared
            right = mid - 1
    return root


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('int_square_root.py',
                                       'int_square_root.tsv', square_root))
