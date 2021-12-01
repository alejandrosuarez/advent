"""
--- Day 9: All in a Single Night ---
Every year, Santa manages to deliver all of his presents in a single night.

This year, however, he has some new locations to visit; his elves have provided him the distances between every pair of locations. He can start and end at any two (different) locations he wants, but he must visit each location exactly once. What is the shortest distance he can travel to achieve this?

For example, given the following distances:

London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141
The possible routes are therefore:

Dublin -> London -> Belfast = 982
London -> Dublin -> Belfast = 605
London -> Belfast -> Dublin = 659
Dublin -> Belfast -> London = 659
Belfast -> Dublin -> London = 605
Belfast -> London -> Dublin = 982
The shortest of these is London -> Dublin -> Belfast = 605, and so the answer is 605 in this example.

What is the distance of the shortest route?
"""

from advent.tools import *


def _dfs(start, graph):
    total_dist = 0
    stack = [(0, start)]
    seen = set()

    while stack:
        dist, cur = stack.pop()

        if cur in seen:
            continue

        seen.add(cur)
        total_dist += dist

        for nei_dist, nei in graph[cur]:
            if nei in seen:
                continue

            stack.append((nei_dist, nei))

    return total_dist, seen


def _pt1(lines):
    graph = cl.defaultdict(set)
    all_cities = set()
    min_dist = float("inf")

    for line in lines:
        src, dest, dist = re.match(r"(\w+) to (\w+) = (\d+)", line).groups()
        dist = int(dist)
        graph[src].add((dist, dest))
        all_cities |= {src, dest}

    for start in list(graph.keys()):
        dist, seen = _dfs(start, graph)
        if not (seen ^ all_cities):
            min_dist = min(dist, min_dist)

    return min_dist


def _pt2(lines):
    pass


TEST = """London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141
"""


def main():
    return afs.input_lines(tests=[TEST], parts=[_pt1], run_input=True)
