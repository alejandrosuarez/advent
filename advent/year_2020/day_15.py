"""
"""

from collections import deque, defaultdict
from advent.util import input_lines

TEST = "0,3,6"


def pt1(arr):
    spoken = arr[:]
    start = len(spoken)
    turns = defaultdict(deque)
    m = 2020

    for i, n in enumerate(spoken):
        turns[n].append(i)

    for i in range(start, m):
        l = spoken[i - 1]
        nxt = 0 if len(turns[l]) < 2 else turns[l][-1] - turns[l][-2]
        spoken.append(nxt)
        turns[nxt].append(i)

        if len(turns[nxt]) > 2:
            turns[nxt].popleft()

    return spoken[-1]


def main():
    parse = lambda s: list(map(int, s.split(",")))
    return pt1(parse(TEST)), pt1(parse(input_lines()[0]))
