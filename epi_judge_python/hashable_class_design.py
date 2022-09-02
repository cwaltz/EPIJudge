"""
#12.0

Consider a class that represents contacts. For simplicity, assume each contact is a string. Suppose
it is a hard requirement that the individual contacts are to be stored in a list, and it's possible that
the list contains duplicates. Two contacts should be equal if they contain the same set of strings,
regardless of the ordering of the strings within the underlying list. Multiplicity is not important,
i.e., three repetitions of the same contact is the same as a single instance of that contact. In order to
be able to store contacts in a hash table, we first need to explicitly define equality which we can do
by forming sets from the lists and comparing the sets.
    In our context, this implies that the hash function should depend on the strings present, but not
their ordering; it should also consider only one copy if a string appears in duplicate form. It should
be pointed out that the hash function and equals methods below are very inefficient. In practice,
it would be advisable to cache the underlying set and the hash code, remembering to void these
values on updates.

The time complexity of computing the hash is O(n), where n is the number of strings in the contact list.
Hash codes are often cached for performance, with the caveat that the cache must be cleared if object fields
that are referenced by the hash function are updated.
"""
from typing import List


class Contactlist:
    def __init__(self, names: List[str]):
        self.names = names

    def __hash__(self):
        # Conceptually we want to hash the set of names. Since the set type is mutable,
        # it cannot be hashed. Therefore, we use frozenset.
        return hash(frozenset(self.names))

    def __eq__(self, other):
        return set(self.names) == set(other.names)


def merge_contact_lists(contacts: List[Contactlist]):
    return list(set(contacts))
