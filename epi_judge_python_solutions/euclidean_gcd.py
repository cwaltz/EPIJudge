from test_framework import generic_test


def gcd(x: int, y: int) -> int:
    """
    Time complexity = O(log max(x, y))
                    = O(n), where n is the number of bits needed to represent the inputs.
    Space complexity = O(n)

    Since with each recursive step one of the arguments is at least halved, it means that the time complexity is
    O(log max(x, y)). Put another way, the time complexity is O(n), where n is the number of bits needed to represent
    the inputs. The space complexity is also O(n), which is the maximum depth of the function call stack.

    Test PASSED (10034/10034) [  <1 us]
    Average running time:    1 us
    Median running time:     1 us
    """
    return x if y == 0 else gcd(y, x % y)


if __name__ == '__main__':
    exit(generic_test.generic_test_main('euclidean_gcd.py', 'gcd.tsv', gcd))
