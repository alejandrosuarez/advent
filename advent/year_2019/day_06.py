"""
"""

from advent.tools import *


def _topological_sort(edges):
    indegrees = {}
    graph = cl.defaultdict(set)
    deps = cl.defaultdict(set)

    for u, v in edges:
        indegrees[u] = 0
        indegrees[v] = 0

    for u, v in edges:
        if v not in graph[u]:
            graph[u].add(v)
            indegrees[v] += 1
            deps[v].add(u)

    q = cl.deque([n for n, i in indegrees.items() if i == 0])
    order = []

    while q:
        node = q.popleft()
        order.append(node)

        for nei in graph[node]:
            indegrees[nei] -= 1
            deps[nei] |= deps[node]

            if indegrees[nei] == 0:
                q.append(nei)

    orbits = sum(len(v) for v in deps.values())
    return orbits


def _pt1(edges):
    return _topological_sort(edges)


def _pt2(edges):
    return _topological_sort(edges)


TEST1 = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L"""

TEST2 = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN"""


def main():
    return afs.input_lines(
        tests=[TEST2],
        parts=[_pt2],
        run_input=False,
        transform_line=lambda l: list(reversed(l.split(")"))),
    )
