from test_framework import generic_test


def num_combinations_for_final_score(final_score: int,
                                     individual_play_scores: list[int]) -> int:
    """
    #16.1

    Time complexity = O(s * n), where s is final score and n is the number of
        individual play scores.
    Space complexity = O(s)

    Test PASSED (1003/1003) [   2 us]
    Average running time:  233 us
    Median running time:   133 us
    """
    # combinations: list[int] = [1] + [0] * final_score  # This line runs
    # slower than the following 2 lines together
    combinations = [0] * (final_score + 1)
    combinations[0] = 1

    for play in individual_play_scores:
        for score in range(play, final_score + 1):
            combinations[score] += combinations[score - play]

    return combinations[final_score]


def num_combinations_for_final_score_with_more_space(
        final_score: int, individual_play_scores: list[int]) -> int:
    """
    Time complexity = O(s * n), where s is final score (= cols) & n is the
    number of individual play scores (= rows).
    Space complexity = O(s * n)

    Test PASSED (1003/1003) [  21 us]
    Average running time:  740 us
    Median running time:   499 us
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
