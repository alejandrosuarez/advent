"""
"""

from advent.tools import *


def _neighbors(r, c, lines):
    m, n = len(lines), len(lines[0])
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
    for y, x in directions:
        nr, nc = r + y, c + x

        if 0 <= nr < m and 0 <= nc < n:
            yield nr, nc


def _step(levels):
    flashes = 0
    for r in range(len(levels)):
        for c in range(len(levels[0])):
            levels[r][c] += 1
    while True:
        cur_flashes = 0
        for r in range(len(levels)):
            for c in range(len(levels[0])):
                if levels[r][c] > 9:
                    levels[r][c] = -levels[r][c]
                    cur_flashes += 1
                    for nr, nc in _neighbors(r, c, levels):
                        if levels[nr][nc] >= 0:
                            levels[nr][nc] += 1
        flashes += cur_flashes
        if not cur_flashes:
            break

    for r in range(len(levels)):
        for c in range(len(levels[0])):
            if levels[r][c] < 0:
                levels[r][c] = 0

    return levels, flashes


def _pt1(levels):
    n = 100
    total_flashes = 0

    for _ in range(n):
        levels, flashes = _step(levels)
        total_flashes += flashes

    return total_flashes


def _pt2(levels):
    step = 1
    n = len(levels) * len(levels[0])
    while True:
        levels, flashes = _step(levels)
        if flashes == n:
            return step
        step += 1


TEST = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
"""
TEST2 = """11111
19991
19191
19991
11111
"""
ANSWERS = [1656, 259, 1721, 195, 6, 298]


def _transform_line(line):
    return list(map(int, line))


def main():
    return afs.input_lines(
        tests=[TEST, TEST2],
        parts=[_pt1, _pt2],
        run_input=True,
        transform_line=_transform_line,
    )
