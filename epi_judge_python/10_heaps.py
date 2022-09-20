"""
#10.0

Heaps boot camp

Each string is processed in O(log k) time, which is the time to add and to
remove the minimum element from the heap. Therefore, if there are n strings
in the input, the time complexity to process all of them is O(n log k). We
could improve best-case time complexity by first comparing the new string's
length with the length of the string at the top of the heap (getting this
string takes O(1) time) and skipping the insert if the new string is too
short to be in the set.
"""

from typing import List
import heapq
import itertools


def top_k(k: int, strings: List[str]) -> List[str]:
    """
    Time complexity = O(n log k), where n is the number of strings in the input.
    Space complexity = O(k).
    """
    # Entries are compared by their lengths.
    min_heap = [(len(string), string)
                for string in itertools.islice(strings, k)]
    heapq.heapify(min_heap)
    for i in range(k, len(strings)):
        # Push next-string and pop the shortest string in min_heap.
        heapq.heappushpop(min_heap, (len(strings[i]), strings[i]))
    return [p[1] for p in heapq.nsmallest(k, min_heap)]


if __name__ == '__main__':
    input_strings = input('Type all the strings: ').split()
    # aniket sagar shivtej akshay omkar soham
    output_size = int(input('How many strings do you want in the output?: '))
    # 2
    result = top_k(output_size, input_strings)
    print(str(output_size), 'longest strings:')
    for s in result:
        print(s)
    # aniket shivtej
