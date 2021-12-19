"""
--- Day 9: Smoke Basin ---
These caves seem to be lava tubes. Parts are even still volcanically active; small hydrothermal vents release smoke into the caves that slowly settles like rain.

If you can model how the smoke flows through the caves, you might be able to avoid it and be that much safer. The submarine generates a heightmap of the floor of the nearby caves for you (your puzzle input).

Smoke flows to the lowest point of the area it's in. For example, consider the following heightmap:

2199943210
3987894921
9856789892
8767896789
9899965678
Each number corresponds to the height of a particular location, where 9 is the highest and 0 is the lowest a location can be.

Your first goal is to find the low points - the locations that are lower than any of its adjacent locations. Most locations have four adjacent locations (up, down, left, and right); locations on the edge or corner of the map have three or two adjacent locations, respectively. (Diagonal locations do not count as adjacent.)

In the above example, there are four low points, all highlighted: two are in the first row (a 1 and a 0), one is in the third row (a 5), and one is in the bottom row (also a 5). All other locations on the heightmap have some lower adjacent location, and so are not low points.

The risk level of a low point is 1 plus its height. In the above example, the risk levels of the low points are 2, 1, 6, and 6. The sum of the risk levels of all low points in the heightmap is therefore 15.

Find all of the low points on your heightmap. What is the sum of the risk levels of all low points on your heightmap?

Your puzzle answer was 524.

--- Part Two ---
Next, you need to find the largest basins so you know what areas are most important to avoid.

A basin is all locations that eventually flow downward to a single low point. Therefore, every low point has a basin, although some basins are very small. Locations of height 9 do not count as being in any basin, and all other locations will always be part of exactly one basin.

The size of a basin is the number of locations within the basin, including the low point. The example above has four basins.

The top-left basin, size 3:

2199943210
3987894921
9856789892
8767896789
9899965678
The top-right basin, size 9:

2199943210
3987894921
9856789892
8767896789
9899965678
The middle basin, size 14:

2199943210
3987894921
9856789892
8767896789
9899965678
The bottom-right basin, size 9:

2199943210
3987894921
9856789892
8767896789
9899965678
Find the three largest basins and multiply their sizes together. In the above example, this is 9 * 14 * 9 = 1134.

What do you get if you multiply together the sizes of the three largest basins?

Your puzzle answer was 1235430.

Both parts of this puzzle are complete! They provide two gold stars: **
"""

from advent.tools import *


def _each_cell(lines):
    for r, row in enumerate(lines):
        for c, val in enumerate(row):
            yield val, r, c, row


def _is_local_minima(val, r, c, row, lines):
    return all(
        [
            c == 0 or val < lines[r][c - 1],
            c == len(row) - 1 or val < lines[r][c + 1],
            r == 0 or val < lines[r - 1][c],
            r == len(lines) - 1 or val < lines[r + 1][c],
        ]
    )


def _pt1(lines):
    minima = []
    for val, r, c, row in _each_cell(lines):
        if _is_local_minima(val, r, c, row, lines):
            minima.append(val)
    return sum(m + 1 for m in minima)


def _neighbors(r, c, lines):
    m, n = len(lines), len(lines[0])
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for y, x in directions:
        nr, nc = r + y, c + x

        if 0 <= nr < m and 0 <= nc < n:
            yield nr, nc


def _pt2(lines):
    starts = []
    sizes = []

    for val, r, c, row in _each_cell(lines):
        if _is_local_minima(val, r, c, row, lines):
            starts.append((r, c))

    for sr, sc in starts:
        q = cl.deque([(sr, sc)])
        seen = set()

        while q:
            r, c = q.popleft()

            if (r, c) in seen:
                continue

            seen.add((r, c))

            for nr, nc in _neighbors(r, c, lines):
                if (nr, nc) in seen:
                    continue
                if lines[nr][nc] == 9:
                    continue
                if lines[nr][nc] <= lines[r][c]:
                    continue
                q.append((nr, nc))

        sizes.append(len(seen))

    return math.prod(sorted(sizes, reverse=True)[:3])


TEST = """2199943210
3987894921
9856789892
8767896789
9899965678
"""
ANSWERS = [15, 524, 1134, 1235430]


def _transform_line(line):
    return list(map(int, line))


def main():
    return afs.input_lines(
        tests=[TEST],
        parts=[_pt1, _pt2],
        run_input=True,
        transform_line=_transform_line,
    )
