import collections
from typing import List, Optional

from test_framework import generic_test
from test_framework.test_failure import TestFailure


class GraphVertex:
    def __init__(self, label: int) -> None:
        self.label = label
        self.edges: List['GraphVertex'] = []


def clone_graph(graph: Optional[GraphVertex]) -> Optional[GraphVertex]:
    """
    #18.5

    DFS, Recursive

    Test PASSED (91/91) [  36 ms]
    Average running time:  522 us
    Median running time:    35 us
    """
    def clone_graph_helper(node: GraphVertex) -> GraphVertex:
        if node in visited:
            return visited[node]
        cloned_node = GraphVertex(node.label)
        visited[node] = cloned_node
        if node.edges:
            cloned_node.edges = [
                clone_graph_helper(edge) for edge in node.edges]
        return cloned_node

    if graph is None:
        return None
    visited = {}
    return clone_graph_helper(graph)


def clone_graph_bfs(graph: Optional[GraphVertex]) -> Optional[GraphVertex]:
    """
    BFS, Iterative

    Test PASSED (91/91) [  35 ms]
    Average running time:  511 us
    Median running time:    34 us
    """
    if graph is None:
        return None
    visited = {graph: GraphVertex(graph.label)}
    queue = collections.deque([graph])
    while queue:
        vertex = queue.popleft()
        for edge in vertex.edges:
            if edge not in visited:
                visited[edge] = GraphVertex(edge.label)
                queue.append(edge)
            visited[vertex].edges.append(visited[edge])
    return visited[graph]


def copy_labels(edges):
    return [e.label for e in edges]


def check_graph(node, graph):
    if node is None:
        raise TestFailure('Graph was not copied')

    vertex_set = set()
    q = collections.deque()
    q.append(node)
    vertex_set.add(node)
    while q:
        vertex = q.popleft()
        if vertex.label >= len(graph):
            raise TestFailure('Invalid vertex label')
        label1 = copy_labels(vertex.edges)
        label2 = copy_labels(graph[vertex.label].edges)
        if sorted(label1) != sorted(label2):
            raise TestFailure('Edges mismatch')
        for e in vertex.edges:
            if e not in vertex_set:
                vertex_set.add(e)
                q.append(e)


def clone_graph_test(k, edges):
    if k <= 0:
        raise RuntimeError('Invalid k value')
    graph = [GraphVertex(i) for i in range(k)]

    for (fr, to) in edges:
        if fr < 0 or fr >= k or to < 0 or to >= k:
            raise RuntimeError('Invalid vertex index')
        graph[fr].edges.append(graph[to])

    result = clone_graph(graph[0])
    check_graph(result, graph)


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('graph_clone.py', 'graph_clone.tsv',
                                       clone_graph_test))
