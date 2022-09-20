"""
#18.0

Graphs boot camp

Graphs are ideal for modeling and analyzing relationships between pairs of
objects. For example, suppose you were given a list of the outcomes of
matches between pairs of teams, with each outcome being a win or loss. A
natural question is as follows: given teams A and B, is there a sequence of
teams starting with A and ending with B such that each team in the sequence
has beaten the next team in the sequence?

A slick way of solving this problem is to model the problem using a graph.
Teams are vertices, and an edge from one team to another indicates that the
team corresponding to the source vertex has beaten the team corresponding to
the destination vertex. Now we can apply graph reachability to perform the
check. Both DFS and BFS are reasonable approaches - the program below uses DFS.

The time complexity and space complexity are both O(E), where E is the number
of outcomes.
"""
import collections

MatchResult = collections.namedtuple('MatchResult', ('winning_team',
                                                     'losing_team'))


def can_team_a_beat_team_b(matches, team_a, team_b):
    """
    Time complexity = O(E), where E is the number of outcomes (= matches).
    Space complexity = O(E)
    """
    def build_graph():
        graph = collections.defaultdict(set)
        for match in matches:
            graph[match.winning_team].add(match.losing_team)
        return graph

    def is_reachable_dfs(graph, curr, dest, visited=set()):
        if curr == dest:
            return True
        elif curr in visited or curr not in graph:
            return False
        visited.add(curr)
        return any(is_reachable_dfs(graph, team, dest) for team in graph[curr])

    return is_reachable_dfs(build_graph(), team_a, team_b)
