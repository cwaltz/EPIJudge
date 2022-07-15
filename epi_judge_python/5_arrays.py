import bisect
import copy

A = [3, 5, 7, 11]
print("A =", A)  # [3, 5, 7, 11]
print("len(A) =", len(A))  # 4
A.append(42)
print("A =", A)  # [3, 5, 7, 11, 42]
A.remove(7)
print("A =", A)  # [3, 5, 11, 42]
A.insert(3, 28)
print("A =", A)  # [3, 5, 11, 28, 42]
B = [1] + [0] * 10
print("B =", B)  # [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

C = list(range(13))
print("C =", C)  # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

D = [[1, 2, 4], [3, 5, 7, 9], [13]]
print("D =", D)  # [[1, 2, 4], [3, 5, 7, 9], [13]]

E = A
F = list(A)
G = copy.copy(A)
H = copy.deepcopy(A)
# TODO: Understand how E, F, G and H differ from each other.

# bisect methods
A = [1, 3, 5, 5, 7, 9]
bisect.bisect_left(A, 5)  # 2
bisect.bisect_right(A, 5)  # 4

# slicing
A = [1, 6, 3, 4, 5, 2, 7]
print(A[2:4])  # [3, 4]
print(A[2:])  # [3, 4, 5, 2, 7]
print(A[:4])  # [1, 6, 3, 4]
print(A[:-1])  # [1, 6, 3, 4, 5, 2]
print(A[-3:])  # [5, 2, 7],
print(A[-3:-1])  # [5, 2]
print(A[1:5:2])  # [6, 4]
print(A[5:1:-2])  # [2, 4]
print(A[::-1])  # [7, 2, 5, 4, 3, 6, 1]  # Reverses list.
# print(A[k:] + A[:k])  # Rotates A by k to the left.
print(A[2:] + A[:2])  # [3, 4, 5, 2, 7, 1, 6] # Rotates A by 2 to the left.
B = A[:]  # Does a (shallow) copy of A into B.

# list comprehension
a = [x ** 2 for x in range(6)]  # yields [0, 1, 4, 9, 16, 25]
b = [x ** 2 for x in range(6) if x % 2 == 0]  # yields [0, 4, 16]

# list comprehension supports multiple levels of looping
A = [1, 3, 5]
Z = ['a', 'b']
C = [(x, y) for x in A for y in Z]  # creates [(1, 'a'), (1, 'b'), (3, 'a'), (3, 'b'), (5, 'a'), (5, 'b')].
# It can also be used to convert a 2D list to a 1D list.
M = [['a', 'b', 'c'], ['d', 'e', 'f']]
print([x for row in M for x in row])  # creates ['a', 'b', 'c', 'd', 'e', 'f '].
# Two levels of looping also allow for iterating over each entry in a 2D list.
A = [[1, 2, 3], [4, 5, 6]]
print([[x**2 for x in row] for row in A])  # yields [[1, 4, 9], [16, 25 , 36]].
