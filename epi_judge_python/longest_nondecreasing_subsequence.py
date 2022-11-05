import bisect
from typing import List

from test_framework import generic_test

"""
Similar to Leetcode # 300. Longest Increasing Subsequence

Difference is leetcode version expects a strictly increasing subsequence whereas
EPI version expects a non-decreasing subsequence.

Source:
https://leetcode.com/problems/longest-increasing-subsequence/solutions/1281811/longest-increasing-subsequence/
One of the best official solutions on Leetcode! <3

https://leetcode.com/problems/longest-increasing-subsequence/solutions/1326308/C++Python-DP-Binary-Search-BIT-Solutions-Picture-explain-O(NlogN)/
One of the best user posts on Leetcode! <3
# TODO: To be fully understood yet!
"""


def longest_nondecreasing_subsequence_length(nums: List[int]) -> int:
    """
    #16.12

    Time complexity = O(n log n), where n = len(nums)
    Space complexity = O(n) for sub array

    Approach 3: Improve Approach 2 With Binary Search
    Explanations:
    https://leetcode.com/problems/longest-increasing-subsequence/solutions/1326308/C++Python-DP-Binary-Search-BIT-Solutions-Picture-explain-O(NlogN)/

    Test PASSED (200/200) [   5 us]
    Average running time:    8 us
    Median running time:     4 us
    """
    sub = []
    for num in nums:  # O(n)
        if not sub or sub[-1] <= num:
            sub.append(num)
        else:  # num < sub[-1]
            # Find the index of the first element > num
            i = bisect.bisect_right(sub, num)  # O(log n)
            # Replace that element with num
            sub[i] = num
    return len(sub)


def longest_nondecreasing_subsequence_length_2(nums: List[int]) -> int:
    """
    Time complexity = O(n ** 2), where n = len(nums)
    Space complexity = O(n) for sub array

    Approach 2: Intelligently Build a Subsequence
    Explanations:
    https://leetcode.com/problems/longest-increasing-subsequence/solutions/1281811/longest-increasing-subsequence/comments/1454083
    https://leetcode.com/problems/longest-increasing-subsequence/discuss/74848/9-lines-C++-code-with-O(NlogN)-complexity/337602

    Test PASSED (200/200) [  11 us]
    Average running time:   21 us
    Median running time:     7 us
    """
    sub = []
    for num in nums:  # O(n)
        if not sub or sub[-1] <= num:
            sub.append(num)
        else:  # num < sub[-1]
            # Find the 1st element in sub that is > num
            for i, n in enumerate(sub):  # O(n)
                if num < n:
                    sub[i] = num
                    break
    return len(sub)


def longest_nondecreasing_subsequence_length_1(nums: List[int]) -> int:
    """
    Time complexity = O(n ** 2), where n = len(nums)
    Space complexity = O(n) for dp array

    Approach 1: Dynamic Programming

    Test PASSED (200/200) [  47 us]
    Average running time:  208 us
    Median running time:    28 us
    """
    dp = [1] * len(nums)
    result = 1
    for i, num in enumerate(nums):  # O(n)
        for j in range(i):  # O(n)
            if nums[j] <= num and dp[i] < dp[j] + 1:
                dp[i] = dp[j] + 1
                if result < dp[i]:
                    result = dp[i]
    return result


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main(
            'longest_nondecreasing_subsequence.py',
            'longest_nondecreasing_subsequence.tsv',
            longest_nondecreasing_subsequence_length))
