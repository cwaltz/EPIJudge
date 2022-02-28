from typing import List
import heapq
import itertools


def top_k(k: int, strings: List[str]) -> List[str]:
    # Entries are compared by their lengths.
    min_heap = [(len(string), string) for string in itertools.islice(strings, k)]
    heapq.heapify(min_heap)
    for i in range(k, len(strings)):
        # Push next-string and pop the shortest string in min_heap.
        heapq.heappushpop(min_heap, (len(strings[i]), strings[i]))
    return [p[1] for p in heapq.nsmallest(k, min_heap)]


if __name__ == '__main__':
    input_strings = input('Type all the strings: ').split()
    # aniket sagar shivtej akshay omkar soham
    k = int(input('How many strings do you want in the output?: '))
    # 2
    result = top_k(k, input_strings)
    print(str(k), 'longest strings:')
    for s in result:
        print(s)
    # aniket shivtej
