from typing import List

from test_framework import generic_test


def num_combinations_for_final_score(final_score: int,
                                     individual_play_scores: List[int]) -> int:
    """
    #16.1

    Time complexity = O(s * n), where s is final score and n is the number of individual play scores.
    Space complexity = O(s)

    Test PASSED (1003/1003) [   3 us]
    Average running time:  355 us
    Median running time:   208 us
    """
    combinations = [1] + [0] * final_score
    for i in range(len(individual_play_scores)):
        for j in range(individual_play_scores[i], final_score + 1):
            combinations[j] += combinations[j - individual_play_scores[i]]
    return combinations[final_score]


def num_combinations_for_final_score_1(final_score: int,
                                       individual_play_scores: List[int]) -> int:
    """
    Time complexity = O(s * n), where s is final score (= cols) & n is the number of individual play scores (= rows).
    Space complexity = O(s * n)

    Test PASSED (1003/1003) [  27 us]
    Average running time:  942 us
    Median running time:   646 us
    """
    # One way to reach 0.
    num_combinations_for_score = [[1] + [0] * final_score
                                  for _ in individual_play_scores]
    for i in range(len(individual_play_scores)):
        for j in range(1, final_score + 1):
            without_this_play = (num_combinations_for_score[i - 1][j]
                                 if i >= 1 else 0)
            with_this_play = (
                num_combinations_for_score[i][j - individual_play_scores[i]]
                if j >= individual_play_scores[i] else 0)
            num_combinations_for_score[i][j] = (without_this_play +
                                                with_this_play)
    return num_combinations_for_score[-1][-1]


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('number_of_score_combinations.py',
                                       'number_of_score_combinations.tsv',
                                       num_combinations_for_final_score))
