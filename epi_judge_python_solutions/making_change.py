from test_framework import generic_test


def change_making(cents: int) -> int:
    """
    Test PASSED (49999/49999) [   1 us]
    Average running time:    1 us
    Median running time:     1 us
    """
    coins = [100, 50, 25, 10, 5, 1]
    num_coins = 0
    for coin in coins:
        num_coins += cents // coin
        cents %= coin
    return num_coins


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('making_change.py', 'making_change.tsv',
                                       change_making))
