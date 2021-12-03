from typing import List

from test_framework import generic_test


def buy_and_sell_stock_once(prices: List[float]) -> float:
    """
    #5.6
    The time complexity is O(n) and the space complexity is O(1), where n is the length of the array.
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
