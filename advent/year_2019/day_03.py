"""
find the intersection point closest to the central port
use manhattan distance
"""

from typing import Tuple
from collections import namedtuple
from itertools import permutations
from advent.util import load_input

UP, DOWN, RIGHT, LEFT = "U", "D", "R", "L"
OPEN, CLOSE, QUERY = 0, 1, 2

Point = namedtuple("Point", ["x", "y"])
Line = namedtuple("Line", ["start", "end"])


def _get_coords(wire):
    coords = [Point(0, 0)]

    for d in wire:
        dxn, dst = d[0], int(d[1:])
        x, y = coords[-1]

        if dxn == UP:
            y += dst
        elif dxn == DOWN:
            y -= dst
        elif dxn == LEFT:
            x -= dst
        elif dxn == RIGHT:
            x += dst

        coords.append(Point(x, y))

    return coords


def _horizontal(l: Line):
    return l.start.y == l.end.y


def _sweep(w1, w2):
    return w1


def _parse_wire(w):
    w = _get_coords(w.split(","))
    w = list(zip(w, w[1:]))
    return [Line(s, e) for s, e in w]


def main():
    wires = [_parse_wire(w) for w in load_input().read().splitlines()]
    intersections = [_sweep(*p) for p in permutations(wires)]

    return intersections