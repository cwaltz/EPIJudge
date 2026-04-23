import functools

from test_framework import generic_test
from test_framework.test_failure import TestFailure
from test_framework.test_utils import enable_executor_hook

NUM_PEGS = 3


def compute_tower_hanoi(num_rings: int) -> list[list[int]]:
    """
    Test PASSED (10/10) [ 195 us]
    Average running time:   40 us
    Median running time:     8 us
    """
    def helper(num: int, src: int, dest: int, aux: int) -> None:
        if num > 1:
            helper(num - 1, src, aux, dest)
        moves.append([src, dest])
        if num > 1:
            helper(num - 1, aux, dest, src)

    moves: list[list[int]] = []
    helper(num_rings, 0, 1, 2)
    return moves


def compute_tower_hanoi_0(num_rings: int) -> list[list[int]]:
    """
    #15.1

    Time complexity = O(2 ** n), where n is the number of rings.
    Space complexity = O(2 ** n) = O(2 ** n) to store the result + O(n) on
        function call stack.

    Test PASSED (10/10) [ 370 us]
    Average running time:   76 us
    Median running time:    19 us
    """

    def compute_tower_hanoi_steps(num_rings_to_move, from_peg, to_peg, use_peg):
        if num_rings_to_move > 0:
            compute_tower_hanoi_steps(num_rings_to_move - 1, from_peg, use_peg,
                                      to_peg)
            pegs[to_peg].append(pegs[from_peg].pop())
            result.append([from_peg, to_peg])
            compute_tower_hanoi_steps(num_rings_to_move - 1, use_peg, to_peg,
                                      from_peg)

    # Initialize pegs.
    result: list[list[int]] = []
    pegs = [list(reversed(range(1, num_rings + 1)))
            ] + [[] for _ in range(1, NUM_PEGS)]
    compute_tower_hanoi_steps(num_rings, 0, 1, 2)
    return result


@enable_executor_hook
def compute_tower_hanoi_wrapper(executor, num_rings):
    pegs = [list(reversed(range(1, num_rings + 1)))
            ] + [[] for _ in range(1, NUM_PEGS)]

    result = executor.run(functools.partial(compute_tower_hanoi, num_rings))

    for from_peg, to_peg in result:
        if pegs[to_peg] and pegs[from_peg][-1] >= pegs[to_peg][-1]:
            raise TestFailure('Illegal move from {} to {}'.format(
                pegs[from_peg][-1], pegs[to_peg][-1]))
        pegs[to_peg].append(pegs[from_peg].pop())
    expected_pegs1 = [[], [], list(reversed(range(1, num_rings + 1)))]
    expected_pegs2 = [[], list(reversed(range(1, num_rings + 1))), []]
    if pegs not in (expected_pegs1, expected_pegs2):
        raise TestFailure('Pegs doesn\'t place in the right configuration')


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('hanoi.py', 'hanoi.tsv',
                                       compute_tower_hanoi_wrapper))
