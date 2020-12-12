"""
find the intersection point closest to the central port
use manhattan distance
"""

from typing import Tuple
from collections import namedtuple
from heapq import heappush, heappop
from itertools import permutations
from shapely.geometry import LineString as Line, Point
from advent.util import load_input

UP, DOWN, RIGHT, LEFT = "U", "D", "R", "L"
OPEN, CLOSE, QUERY = 0, 1, 2

Event = namedtuple("Event", ["time", "id", "line"])


def _get_coords(wire):
    coords = [Point(0, 0)]

    for d in wire:
        dxn, dst = d[0], int(d[1:])
        p = coords[-1]
        x, y = p.x, p.y

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


def _vertical(l: Line):
    return l.coords[0][1] != l.coords[1][1]


def _sweep(w1, w2):
    events, live, intersections = [], {}, []

    for i, line in enumerate(w1):
        if _vertical(line):
            continue

        heappush(events, Event(line.coords[0][0], i, line))
        heappush(events, Event(line.coords[1][0], i, line))

    for i, line in enumerate(w2):
        if not _vertical(line):
            continue

        heappush(events, Event(line.coords[0][0], i + len(w1), line))

    while events:
        e = heappop(events)
        sweep = e.time

        if _vertical(e.line):
            for candidate in live.values():
                if candidate.crosses(e.line):
                    intersections.append(candidate.intersection(e.line))
        elif sweep == e.line.coords[0][0]:
            live[id(e.line)] = e.line
        elif sweep == e.line.coords[1][0]:
            del live[id(e.line)]

    return intersections


def _parse_wire(w):
    w = _get_coords(w.split(","))
    w = list(zip(w, w[1:]))
    return [Line([a, b]) if a.x < b.x else Line([b, a]) for i, (a, b) in enumerate(w)]


def main():
    wires = [_parse_wire(w) for w in load_input().read().splitlines()]
    intersections = [_sweep(*p) for p in permutations(wires)]
    intersections = [i for s in intersections for i in s]
    ans = min(intersections, key=lambda i: abs(i.x) + abs(i.y))

    return int(abs(ans.x) + abs(ans.y))