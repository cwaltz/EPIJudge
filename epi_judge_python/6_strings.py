print("'Euclid,Axiom 5,Parallel Lines'.split(',') =", 'Euclid,Axiom 5,Parallel Lines'.split(','))
# ['Euclid', 'Axiom 5', 'Parallel Lines']

print("'Euclid,Axiom 5,Parallel Lines'.split(' ') =", 'Euclid,Axiom 5,Parallel Lines'.split(' '))
# ['Euclid,Axiom', '5,Parallel', 'Lines']

print("3 * '01' =", 3 * '01')
# '010101'

print("','.join(('Gauss', 'Prince of Mathematicians', '1777-1855')) =",
      ','.join(('Gauss', 'Prince of Mathematicians', '1777-1855')))  # 'Gauss,Prince of Mathematicians,1777-1855'

print("'Name {name}, Rank {rank}'.format(name='Archimedes', rank=3) =",
      'Name {name}, Rank {rank}'.format(name='Archimedes', rank=3))  # 'Name Archimedes, Rank 3'
