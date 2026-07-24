"""
Important Note:

There are a lot of different ways to solve this well-known problem and the top
approaches have been implemented below with inputs from Gemini. Understanding
the recursive backtracking solution and the obvious followup questions and
their solutions is a MUST.

The rest can be done if time allows.
"""


import itertools
import math
from collections.abc import Iterator

from test_framework import generic_test, test_utils


def generate_power_set_interview(input_set: list[int]) -> list[list[int]]:
    """
    #15.4

    Time complexity = O(n * (2 ** n)), where n is the length of input_set.
    Space complexity = O(n)

    Standard interview backtracking solution. Avoids unnecessary list creations
    by maintaining a single state vector and yielding deep copies.

    Test PASSED (15/15) [   5 ms]
    Average running time:  777 us
    Median running time:    43 us
    """

    def backtrack(start_index: int, current_subset: list[int]) -> None:
        # Append a snapshot (copy) of the current state
        power_set.append(list(current_subset))

        for i in range(start_index, length):
            # 1. Choose: Include the current element
            current_subset.append(input_set[i])

            # 2. Explore: Recurse with the next index
            backtrack(i + 1, current_subset)

            # 3. Un-choose: Backtrack by removing the element
            current_subset.pop()

    power_set: list[list[int]] = []
    length = len(input_set)
    backtrack(0, [])
    return power_set


# Below are 3 of the most obvious followup questions and solutions to them


def generate_subsets_of_size_k(input_set: list[int], k: int) -> list[list[int]]:
    """
    Extension 1: Subsets of Exactly Size K

    By using backtracking, we can aggressively optimize this. Instead of
    generating the full power set and filtering it, we add pruning. We stop
    recursing if the subset reaches size k, and we abandon loops early if there
    aren't enough elements left in the array to reach size k.
    """
    def backtrack(start_index: int, current_subset: list[int]) -> None:
        # Base case: subset reached desired size
        if len(current_subset) == k:
            result.append(list(current_subset))
            return

        for i in range(start_index, length):
            # Pruning optimization: if there aren't enough elements left
            # in the array to reach size k, stop exploring this branch.
            if len(current_subset) + (length - i) < k:
                break

            current_subset.append(input_set[i])
            backtrack(i + 1, current_subset)
            current_subset.pop()

    result: list[list[int]] = []
    length = len(input_set)
    backtrack(0, [])
    return result


def generate_unique_power_set(input_set: list[int]) -> list[list[int]]:
    """
    Extension 2: Input Contains Duplicates (Unique Subsets Only)

    If the input is [1, 2, 2], the standard algorithm would output two
    identical [1, 2] subsets. To fix this without resorting to an inefficient
    set() cast at the end, we sort the array and skip identical adjacent
    elements at the same depth of the recursion tree.
    """
    def backtrack(start_index: int, current_subset: list[int]) -> None:
        result.append(list(current_subset))

        for i in range(start_index, length):
            # Skip duplicates at the same level of the decision tree
            if i > start_index and input_set[i] == input_set[i - 1]:
                continue

            current_subset.append(input_set[i])
            backtrack(i + 1, current_subset)
            current_subset.pop()

    result: list[list[int]] = []
    # Sorting is required so duplicates sit adjacent to each other
    input_set.sort()
    length = len(input_set)
    backtrack(0, [])
    return result


def generate_power_set_lazy(input_set: list[int]) -> Iterator[list[int]]:
    """
    Extension 3: Input is Too Large (Lazy Evaluation / Iterator)

    If memory is constrained, returning a massive list[list[int]] will crash
    the system. We convert the function into a generator using yield and yield
    from. This maintains the O(1) auxiliary memory footprint (aside from the
    call stack) because subsets are yielded one by one and garbage collected
    after the caller consumes them.

    TODO: To be understood yet
    """

    def backtrack(
            start_index: int, current_subset: list[int]) -> Iterator[list[int]]:
        # Yield the current state to the caller
        yield list(current_subset)

        for i in range(start_index, length):
            current_subset.append(input_set[i])

            # Delegate generation to the recursive call
            yield from backtrack(i + 1, current_subset)

            current_subset.pop()

    length = len(input_set)
    # Initiate the generator chain
    yield from backtrack(0, [])


# The following are the various solutions to the original problem


def generate_power_set_iterative_dfs(input_set: list[int]) -> list[list[int]]:
    """
    Test PASSED (15/15) [   8 ms]
    Average running time:    1 ms
    Median running time:    72 us

    TODO: To be understood yet
    """
    result: list[list[int]] = []

    # Stack stores tuples of: (start_index, current_subset)
    stack = [(0, [])]

    while stack:
        start_index, current_subset = stack.pop()

        # In this explicit stack model, the state is already a unique list,
        # so we can append it directly without copying.
        result.append(current_subset)

        # To mimic the exact same output order as recursive DFS,
        # we iterate backwards so the smallest indices are popped first.
        for i in range(len(input_set) - 1, start_index - 1, -1):
            # We create a new list for the next state, just like
            # parameter passing does in recursion.
            next_state = current_subset + [input_set[i]]
            stack.append((i + 1, next_state))

    return result


def generate_power_set_enterprise(input_set: list[int]) -> list[list[int]]:
    """
    Enterprise-ready implementation using CPython's highly optimized itertools.
    We convert the returned tuples back to lists to satisfy the strict
    signature.

    Test PASSED (15/15) [   2 ms]
    Average running time:  472 us
    Median running time:    24 us

    TODO: To be understood yet
    """
    power_set: list[list[int]] = []

    # Iterate through all possible subset sizes (0 to N)
    for r in range(len(input_set) + 1):
        # itertools.combinations yields tuples, so we map them to lists
        power_set.extend(
            list(combo) for combo in itertools.combinations(input_set, r))

    return power_set


def generate_power_set_bitwise(input_set: list[int]) -> list[list[int]]:
    """
    Bitwise approach without floating-point math risks.
    Uses two's complement and integer bit lengths to find indices safely.

    Test PASSED (15/15) [  18 ms]
    Average running time:    2 ms
    Median running time:    69 us

    TODO: To be understood yet
    """
    power_set: list[list[int]] = []
    length = len(input_set)

    for i in range(1 << length):
        subset: list[int] = []
        bit_array = i

        while bit_array:
            # Isolate the lowest set bit using two's complement
            # (equivalent to x & ~(x-1))
            lsb = bit_array & -bit_array

            # Find the index of that bit using integer math
            index = lsb.bit_length() - 1
            subset.append(input_set[index])

            # Clear the lowest set bit
            bit_array &= (bit_array - 1)

        power_set.append(subset)

    return power_set


def generate_power_set_bitwise_1(input_set: list[int]) -> list[list[int]]:
    """
    Test PASSED (15/15) [  22 ms]
    Average running time:    2 ms
    Median running time:    88 us

    TODO: To be understood yet
    """
    n = len(input_set)
    power_set = []

    # Iterate from 0 to (2^n - 1)
    limit = 1 << n
    for i in range(limit):
        subset = []
        # Check each bit position j
        for j in range(n):
            if i & (1 << j):
                subset.append(input_set[j])
        power_set.append(subset)

    return power_set


# Old solutions


def generate_power_set_pythonic(input_set: list[int]) -> list[list[int]]:
    """
    Time complexity = O(n * (2 ** n)), where n is the length of input_set.
    Space complexity = O(n * (2 ** n))

    Test PASSED (15/15) [   2 ms]
    Average running time:  340 us
    Median running time:    13 us
    """
    power_set = [[]]
    for i in input_set:
        power_set += [item + [i] for item in power_set]
    return power_set


def generate_power_set_interview_old(input_set: list[int]) -> list[list[int]]:
    """
    Recursive solution

    Time complexity = O(n * (2 ** n)), where n is the length of input_set.
    Space complexity = O(n * (2 ** n))

    The number of recursive calls, C(n) satisfies the recurrence
    C(n) = 2C(n - 1), which solves to C(n) = O(2 ** n).
    Since we spend O(n) time within a call,
    the time complexity is O(n * (2 ** n)).
    The space complexity is O(n * (2 ** n)), since there are 2 ** n subsets,
    and the average subset size is n / 2.

    Test PASSED (15/15) [   5 ms]
    Average running time:  847 us
    Median running time:    46 us

    TODO: To be understood yet
    """

    # Generate all subsets whose intersection with input_set[0], ...,
    # input_set[to_be_selected - 1] is exactly selected_so_far.
    def directed_power_set(to_be_selected: int, selected_so_far: list[int]):
        if to_be_selected == len(input_set):
            power_set.append(selected_so_far)
            return

        directed_power_set(to_be_selected + 1, selected_so_far)
        # Generate all subsets that contain input_set[to_be_selected].
        directed_power_set(to_be_selected + 1,
                           selected_so_far + [input_set[to_be_selected]])

    power_set: list[list[int]] = []
    directed_power_set(0, [])
    return power_set


def generate_power_set_bitwise_old(input_set: list[int]) -> list[list[int]]:
    """
    Time complexity = O(n * (2 ** n)), where n is the length of input_set.
    Space complexity = O(n * (2 ** n))

    Since each set takes O(n) time to compute, the time complexity is
    O(n * (2 ** n)).
    In practice, this approach is very fast. Furthermore, its space complexity
    is O(n) when we want to just enumerate
    subsets, e.g., to print them, rather that to return all the subsets.

    Test PASSED (15/15) [  23 ms]
    Average running time:    3 ms
    Median running time:    83 us

    TODO: To be understood yet
    """
    power_set: list[list[int]] = []
    for int_for_subset in range(1 << len(input_set)):
        bit_array = int_for_subset
        subset = []
        while bit_array:
            subset.append(
                input_set[int(math.log2(bit_array & ~(bit_array - 1)))])
            bit_array &= (bit_array - 1)
        power_set.append(subset)
    return power_set


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main(
            'power_set.py', 'power_set.tsv',
            generate_power_set_interview, test_utils.unordered_compare))
