import math


print("6 & 4 = " + str(6 & 4))  # 4
print("1 | 2 = " + str(1 | 2))  # 3
print("8 >> 1 = " + str(8 >> 1))  # 4
print("-16 >> 2 = " + str(-16 >> 2))  # -4
print("1 << 10 = " + str(1 << 10))  # 1024
print("~0 = " + str(~0))  # -1
print("~1 = " + str(~1))  # -2
print("15 ^ 10 = " + str(15 ^ 10))  # 5
print("abs(-34.5) =", abs(-34.5))  # 34.5

print("math.ceil(2.17) =", math.ceil(2.17))  # 3
print("math.ceil(-2.17) =", math.ceil(-2.17))  # -2
print("math.floor(3.14) =", math.floor(3.14))  # 3
print("math.floor(-3.14) =", math.floor(-3.14))  # -4
print("pow(2.71, 3.14) =", pow(2.71, 3.14))  # 22.883559193263366
print("pow(2, 3) =", pow(2, 3))  # 8
print("3 ** 2 =", 3 ** 2)  # 9
print("math.sqrt(225) =", math.sqrt(225))  # 15.0


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
    pass


def test_if_x_is_a_power_of_2(x: int) -> bool:
    """
    Write expressions that use bitwise operators, equality checks, and Boolean operators to do the following in O(1)
    time.
    Test if x is a power of 2, i.e., evaluates to true for x = 1, 2, 4, 8,..., false for all other values.
    """
    if (x <= 0) or (x & (x - 1) != 0):
        return False
    return True
