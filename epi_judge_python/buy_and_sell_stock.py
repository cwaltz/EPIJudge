from typing import List

from test_framework import generic_test


def buy_and_sell_stock_once(prices: List[float]) -> float:
    """
    #5.6

    Time complexity = O(n), where n is the length of the array.
    Space complexity = O(1)

    Test PASSED (402/402) [   4 ms]
    Average running time:   28 us
    Median running time:     3 us
    """
    min_so_far = prices[0]
    max_profit = 0.0
    for price in prices:
        if price < min_so_far:
            min_so_far = price
        if max_profit < price - min_so_far:
            max_profit = price - min_so_far
    return max_profit


def buy_and_sell_stock_once1(prices: List[float]) -> float:
    """
    #5.6
    The time complexity is O(n) and the space complexity is O(1), where n is the length of the array.

    Test PASSED (402/402) [  17 ms]
    Average running time:  113 us
    Median running time:    11 us
    """
    min_price, max_profit = float('inf'), 0.0
    for price in prices:
        profit = price - min_price
        max_profit = max(max_profit, profit)
        min_price = min(min_price, price)
    return max_profit


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('buy_and_sell_stock.py',
                                       'buy_and_sell_stock.tsv',
                                       buy_and_sell_stock_once))
