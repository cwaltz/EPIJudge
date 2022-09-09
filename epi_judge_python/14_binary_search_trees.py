import bintrees
import sortedcontainers

"""
#14.0

Binary Search Trees boot camp
"""

t = bintrees.RBTree([(5, 'Alfa'), (2, 'Bravo'), (7, 'Charlie'), (3, 'Delta'), (6, 'Echo')])
# t1 = sortedcontainers.SortedList([(5, 'Alfa'), (2, 'Bravo'), (7, 'Charlie'), (3, 'Delta'), (6, 'Echo')])

print(t[2])  # 'Bravo'

print(t.min_item(), t.max_item())  # (2, 'Bravo'), (7, 'Charlie')

# {2: 'Bravo', 3: 'Delta', 5: 'Alfa', 6: 'Echo', 7: 'Charlie', 9: 'Golf'}
t.insert(9, 'Golf')
print(t)

print(t.min_key(), t.max_key())  # 2, 9

t.discard(3)
print(t)  # {2: 'Bravo', 5: 'Alfa', 6: 'Echo', 7: 'Charlie', 9: 'Golf'}

# a = (2: 'Bravo')
a = t.pop_min()
print(t)  # {5: 'Alfa', 6: 'Echo', 7: 'Charlie', 9: 'Golf'}

# b = (9, 'Golf')
b = t.pop_max()
print(t)  # {5: 'Alfa', 6: 'Echo', 7: 'Charlie'}
