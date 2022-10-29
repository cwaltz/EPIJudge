from typing import List

from test_framework import generic_test


def buy_and_sell_stock_once(prices: List[float]) -> float:
    """
    #5.6

    Time complexity = O(n), where n = len(prices)
    Space complexity = O(1)

    Test PASSED (402/402) [   3 ms]
    Average running time:   17 us
    Median running time:     2 us
    """
    min_price, max_profit = prices[0], 0.0
    for price in prices:
        if price < min_price:
            min_price = price
        elif max_profit < price - min_price:
            max_profit = price - min_price
    return max_profit


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('buy_and_sell_stock.py',
                                       'buy_and_sell_stock.tsv',
                                       buy_and_sell_stock_once))
