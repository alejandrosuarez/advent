"""
--- Day 3: Crossed Wires ---
The gravity assist was successful, and you're well on your way to the Venus refuelling station.
During the rush back on Earth, the fuel management system wasn't completely installed, so that's next on the priority list.

Opening the front panel reveals a jumble of wires. Specifically, two wires are connected to a central port
and extend outward on a grid. You trace the path each wire takes as it leaves the central port,
one wire per line of text (your puzzle input).

The wires twist and turn, but the two wires occasionally cross paths. To fix the circuit, you need to
find the intersection point closest to the central port. Because the wires are on a grid, use the
Manhattan distance for this measurement. While the wires do technically cross right at the central port
where they both start, this point does not count, nor does a wire count as crossing with itself.

For example, if the first wire's path is R8,U5,L5,D3, then starting from the central port (o),
it goes right 8, up 5, left 5, and finally down 3:

...........
...........
...........
....+----+.
....|....|.
....|....|.
....|....|.
.........|.
.o-------+.
...........
Then, if the second wire's path is U7,R6,D4,L4, it goes up 7, right 6, down 4, and left 4:

...........
.+-----+...
.|.....|...
.|..+--X-+.
.|..|..|.|.
.|.-X--+.|.
.|..|....|.
.|.......|.
.o-------+.
...........
These wires cross at two locations (marked X), but the lower-left one is closer to the central port: its distance is 3 + 3 = 6.

Here are a few more examples:

R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83 = distance 159
R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
U98,R91,D20,R16,D67,R40,U7,R15,U6,R7 = distance 135
What is the Manhattan distance from the central port to the closest intersection?

Your puzzle answer was 1211.

--- Part Two ---
It turns out that this circuit is very timing-sensitive; you actually need to minimize the signal delay.

To do this, calculate the number of steps each wire takes to reach each intersection; choose the
intersection where the sum of both wires' steps is lowest. If a wire visits a position on the grid multiple times,
use the steps value from the first time it visits that position when calculating the total value of a specific intersection.

The number of steps a wire takes is the total number of grid squares the wire has entered to get to that location,
including the intersection being considered. Again consider the example from above:

...........
.+-----+...
.|.....|...
.|..+--X-+.
.|..|..|.|.
.|.-X--+.|.
.|..|....|.
.|.......|.
.o-------+.
...........
In the above example, the intersection closest to the central port is reached after 8+5+5+2 = 20 steps
by the first wire and 7+6+4+3 = 20 steps by the second wire for a total of 20+20 = 40 steps.

However, the top-right intersection is better: the first wire takes only 8+5+2 = 15 and the second wire
takes only 7+6+2 = 15, a total of 15+15 = 30 steps.

Here are the best steps for the extra examples from above:

R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83 = 610 steps
R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
U98,R91,D20,R16,D67,R40,U7,R15,U6,R7 = 410 steps
What is the fewest combined steps the wires must take to reach an intersection?

Your puzzle answer was 101386.

Both parts of this puzzle are complete! They provide two gold stars: **
"""

from shapely.geometry import LineString as Line
from shapely.geometry import Point

from advent.tools import *

UP, DOWN, RIGHT, LEFT = "U", "D", "R", "L"
OPEN, CLOSE, QUERY = 0, 1, 2

Event = cl.namedtuple("Event", ["time", "id", "line"])


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

        hq.heappush(events, Event(line.coords[0][0], i, line))
        hq.heappush(events, Event(line.coords[1][0], i, line))

    for i, line in enumerate(w2):
        if not _vertical(line):
            continue

        hq.heappush(events, Event(line.coords[0][0], i + len(w1), line))

    while events:
        e = hq.heappop(events)
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


def _intersections(wires):
    intersections = [_sweep(*p) for p in it.permutations(wires)]
    return [i for s in intersections for i in s]


def _manhattan_distance(point):
    return abs(point.x) + abs(point.y)


def _build_line(a, b):
    l = Line([a, b]) if a.x < b.x else Line([b, a])
    l.start, l.end = a, b
    return l


def _lines(wires):
    for points in wires:
        w = list(zip(points, points[1:]))
        yield [_build_line(a, b) for a, b in w]


def _pt2(wires):
    lines = list(_lines(wires))
    intersections = _intersections(lines)
    steps = cl.defaultdict(int)

    for l in lines:
        cur, last = 0, None

        for line in l:
            cur += line.length

            for i in intersections:
                if line.contains(i):
                    diff = abs(line.end.distance(i))
                    steps[tuple(i.coords)] += cur - diff

    return int(min(steps.values()))


def _pt1(wires):
    lines = list(_lines(wires))
    return int(min(list(map(_manhattan_distance, _intersections(lines)))))


TEST1 = """R8,U5,L5,D3
U7,R6,D4,L4"""

TEST2 = """R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83"""

TEST3 = """R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"""

ANSWERS = [6, 159, 135, 1211, 30, 610, 410, 101386]


def main():
    tr = lambda l: _get_coords(l.split(","))

    return afs.input_lines(
        tests=[TEST1, TEST2, TEST3],
        parts=[_pt1, _pt2],
        transform_line=tr,
    )
