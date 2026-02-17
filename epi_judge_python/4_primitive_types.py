import math


print(f"6 & 4 = {6 & 4}")  # 4
print(f"1 | 2 = {1 | 2}")  # 3
print(f"8 >> 1 = {8 >> 1}")  # 4
print(f"-16 >> 2 = {-16 >> 2}")  # -4
print(f"1 << 10 = {1 << 10}")  # 1024
print(f"~0 = {~0}")  # -1
print(f"~1 = {~1}")  # -2
print(f"15 ^ 10 = {15 ^ 10}")  # 5
print(f"abs(-34.5) = {abs(-34.5)}")  # 34.5

print(f"math.ceil(2.17) = {math.ceil(2.17)}")  # 3
print(f"math.ceil(-2.17) = {math.ceil(-2.17)}")  # -2
print(f"math.floor(3.14) = {math.floor(3.14)}")  # 3
print(f"math.floor(-3.14) = {math.floor(-3.14)}")  # -4
print(f"pow(2.71, 3.14) = {pow(2.71, 3.14)}")  # 22.883559193263366
print(f"pow(2, 3) = {pow(2, 3)}")  # 8
print(f"3 ** 2 = {3 ** 2}")  # 9
print(f"math.sqrt(225) = {math.sqrt(225)}")  # 15.0


def right_propagate_rightmost_set_bit(x: int) -> int:
    """
    Write expressions that use bitwise operators, equality checks, and Boolean operators to do the following in O(1)
    time.
    Right propagate the rightmost set bit in x, e.g., turns (01010000)2 to (01011111)2.
    """
    result = 0
    if x:
        result = x | (x - 1)
    return result


def compute_x_modulo_a_power_of_two(x: int) -> int:
    """
    Write expressions that use bitwise operators, equality checks, and Boolean operators to do the following in O(1)
    time.
    Compute x modulo a power of two, e.g., returns 13 for 77 mod 64.
    """
    highest_power_of_2 = 1 << (x.bit_length() - 1)
    return x ^ highest_power_of_2


def test_if_x_is_a_power_of_2(x: int) -> bool:
    """
    Write expressions that use bitwise operators, equality checks, and Boolean operators to do the following in O(1)
    time.
    Test if x is a power of 2, i.e., evaluates to true for x = 1, 2, 4, 8,..., false for all other values.
    """
    if (x <= 0) or (x & (x - 1) != 0):
        return False
    return True
