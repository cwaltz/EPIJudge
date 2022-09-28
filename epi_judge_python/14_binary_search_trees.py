"""
#14.0

Binary Search Trees boot camp
"""
import bintrees
import sortedcontainers

t = bintrees.RBTree([(5, 'Alfa'), (2, 'Bravo'), (7, 'Charlie'), (3, 'Delta'),
                     (6, 'Echo')])
t1 = sortedcontainers.SortedDict({5: 'Alfa', 2: 'Bravo', 7: 'Charlie',
                                  3: 'Delta', 6: 'Echo'})

print(t[2])  # 'Bravo'
print(t1.get(2))  # 'Bravo'

print(t.min_item(), t.max_item())  # (2, 'Bravo'), (7, 'Charlie')
print(t1.items()[0], t1.items()[-1])  # (2, 'Bravo'), (7, 'Charlie')

# {2: 'Bravo', 3: 'Delta', 5: 'Alfa', 6: 'Echo', 7: 'Charlie', 9: 'Golf'}
t.insert(9, 'Golf')
print(t)
t1.setdefault(9, 'Golf')
print(t1)

print(t.min_key(), t.max_key())  # 2, 9
print(t1.keys()[0], t1.keys()[-1])  # 2, 9

t.discard(3)
print(t)  # {2: 'Bravo', 5: 'Alfa', 6: 'Echo', 7: 'Charlie', 9: 'Golf'}
t1.pop(3)
print(t1)  # {2: 'Bravo', 5: 'Alfa', 6: 'Echo', 7: 'Charlie', 9: 'Golf'}

# a = (2: 'Bravo')
a = t.pop_min()
print(t)  # {5: 'Alfa', 6: 'Echo', 7: 'Charlie', 9: 'Golf'}
a1 = t1.popitem(0)
print(t1)  # {5: 'Alfa', 6: 'Echo', 7: 'Charlie', 9: 'Golf'}

# b = (9, 'Golf')
b = t.pop_max()
print(t)  # {5: 'Alfa', 6: 'Echo', 7: 'Charlie'}
b1 = t1.popitem(-1)
print(t1)  # {5: 'Alfa', 6: 'Echo', 7: 'Charlie'}
