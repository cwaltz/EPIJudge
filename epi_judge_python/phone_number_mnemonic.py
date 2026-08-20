import itertools

from test_framework import generic_test, test_utils

# The mapping from digit to corresponding characters.
MAPPING = ('0', '1', 'ABC', 'DEF', 'GHI', 'JKL', 'MNO', 'PQRS', 'TUV', 'WXYZ')


def phone_mnemonic_interview(phone_number: str) -> list[str]:
    """
    #6.7

    This is the classic Depth-First Search (DFS) backtracking approach using a
    nested helper function.

    Pros: This is the gold standard for a software engineering interview. It
    perfectly demonstrates your understanding of recursive state trees, base
    cases, and in-place array manipulation.
    By initializing partial_mnemonic = ['0'] * len(...) and overwriting indices,
    you save vast amounts of memory compared to the iterative approach.

    Cons: Slower in Python than itertools due to the overhead of recursive
    function calls.

    Verdict: Perfect for interviews.

    Time complexity  = O((4 ** n) * n), where n = length(phone_number)
    Space complexity = O((4 ** n) * n)

    Test PASSED (102/102) [   2 ms]
    Average running time:   80 us
    Median running time:    11 us
    """

    def phone_mnemonic_helper(digit: int) -> None:
        if digit == len(phone_number):
            # All digits are processed, so add partial_mnemonic to mnemonics.
            # (We add a copy since subsequent calls modify partial_mnemonic.)
            mnemonics.append(''.join(partial_mnemonic))
        else:
            # Try all possible characters for this digit.
            for letter in MAPPING[int(phone_number[digit])]:
                partial_mnemonic[digit] = letter
                phone_mnemonic_helper(digit + 1)

    if not phone_number.isdigit():
        raise ValueError("Phone number must contain only digits.")

    mnemonics: list[str] = []
    partial_mnemonic = ['0'] * len(phone_number)
    phone_mnemonic_helper(0)
    return mnemonics


# Pythonic solution
def phone_mnemonic_production(phone_number: str) -> list[str]:
    """
    # TODO: To be fully understood yet.

    Clean, highly readable, and delegates the heavy lifting to Python's
    underlying C API, making it the most performant and memory-efficient.
    The absolute winner for Enterprise Production but not recommended for
    interviews.

    Test PASSED (102/102) [   1 ms]
    Average running time:   33 us
    Median running time:     5 us
    """
    return [
        ''.join(mnemonic)
        for mnemonic in itertools.product(*(MAPPING[int(digit)]
                                            for digit in phone_number))
    ]

    # # A visually more readable version of the above one-liner
    # return [
    #     ''.join(mnemonic)
    #     for mnemonic
    #     in itertools.product(
    #         *(
    #             MAPPING[int(digit)]
    #             for digit
    #             in phone_number
    #         )
    #     )
    # ]


def phone_mnemonic_iterative_stack(phone_number: str) -> list[str]:
    """
    Test PASSED (102/102) [   4 ms]
    Average running time:  122 us
    Median running time:    18 us
    """
    if not phone_number:
        return []
    if not phone_number.isdigit():
        raise ValueError("Phone number must contain only digits.")

    mnemonics: list[str] = []

    # The stack holds tuples of (current_index, partial_mnemonic_list)
    initial_mnemonic = ['0'] * len(phone_number)
    stack = [(0, initial_mnemonic)]

    while stack:
        digit, partial_mnemonic = stack.pop()

        if digit == len(phone_number):
            # Base case reached: all digits processed
            mnemonics.append(''.join(partial_mnemonic))
        else:
            # Iterate in reverse to maintain standard DFS left-to-right order
            letters = MAPPING[int(phone_number[digit])]
            for letter in reversed(letters):
                # We MUST copy the list;
                # otherwise, branches overwrite each other
                new_mnemonic = partial_mnemonic[:]
                new_mnemonic[digit] = letter
                stack.append((digit + 1, new_mnemonic))

    return mnemonics


def phone_mnemonic(phone_number: str) -> list[str]:
    """
    Test PASSED (102/102) [   3 ms]
    Average running time:   75 us
    Median running time:    10 us
    """
    if not phone_number.isdigit():
        raise ValueError("Phone number must contain only digits.")

    curr_sequences = [[]]
    for digit in phone_number:
        next_sequences = []
        for letter in MAPPING[int(digit)]:
            for sequence in curr_sequences:
                next_sequences.append(sequence + [letter])
        curr_sequences = next_sequences

    return [''.join(sequence) for sequence in curr_sequences]


def phone_mnemonic_pythonic_another(phone_number: str) -> list[str]:
    """
    Test PASSED (102/102) [  10 ms]
    Average running time:  302 us
    Median running time:    38 us
    """
    table = {
        '0': '0',
        '1': '1',
        '2': 'ABC',
        '3': 'DEF',
        '4': 'GHI',
        '5': 'JKL',
        '6': 'MNO',
        '7': 'PQRS',
        '8': 'TUV',
        '9': 'WXYZ'
    }
    return [
        a + b for a in table.get(phone_number[:1], '')
        for b in phone_mnemonic_pythonic_another(phone_number[1:]) or ['']
    ]


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main(
            'phone_number_mnemonic.py',
            'phone_number_mnemonic.tsv',
            phone_mnemonic_iterative_stack,
            comparator=test_utils.unordered_compare))
