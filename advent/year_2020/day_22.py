"""
"""

from advent.tools import *

TEST = """Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10"""


def _pt1(starting):
    p1, p2 = starting

    while p1 and p2:
        c1, c2 = p1.popleft(), p2.popleft()

        if c1 > c2:
            p1.extend([c1, c2])
        else:
            p2.extend([c2, c1])

    return sum(c * (i + 1) for i, c in enumerate(list(p1 or p2)[::-1]))


def _parse(r):
    return [cl.deque(list(map(int, s.splitlines()[1:]))) for s in r]


def main():
    t = _parse(TEST.split("\n\n"))
    s = _parse(afs.read_input().split("\n\n"))
    return _pt1(t), _pt1(s)
