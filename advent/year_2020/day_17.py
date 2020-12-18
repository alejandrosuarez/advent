"""
"""

from advent.util import input_lines
import numpy as np
from itertools import product
from copy import deepcopy

TEST = """.#.
..#
###"""

ACTIVE, INACTIVE = 1, 0
MAPPING = {"#": ACTIVE, ".": INACTIVE}
DIRECTIONS = list(product([+1, -1, 0], repeat=3))[:-1]


def _expand_grid(grid):
    m, n = len(grid[0]) + 2, len(grid[0][0]) + 2

    return (
        [[[INACTIVE for _ in range(n)] for _ in range(m)]]
        + [
            [[INACTIVE for _ in range(n)]]
            + [[INACTIVE] + r + [INACTIVE] for r in z]
            + [[INACTIVE for _ in range(n)]]
            for z in grid
        ]
        + [[[INACTIVE for _ in range(n)] for _ in range(m)]]
    )


def _game_of_life(grid, cycles=6):
    last = None

    for _ in range(cycles):
        grid = _expand_grid(grid)
        last = deepcopy(grid)
        o, m, n = len(grid), len(grid[0]), len(grid[0][0])

        for i, z in enumerate(grid):
            for j, r in enumerate(z):
                for k, c in enumerate(r):
                    active = 0

                    for d1, d2, d3 in DIRECTIONS:
                        nz, ny, nx = i + d1, j + d2, k + d3

                        if (
                            0 <= nz < o
                            and 0 <= ny < m
                            and 0 <= nx < n
                            and last[nz][ny][nx] == ACTIVE
                        ):
                            active += 1

                    if last[i][j][k] == ACTIVE:
                        if active not in {2, 3}:
                            grid[i][j][k] = INACTIVE
                    else:
                        if active == 3:
                            grid[i][j][k] = ACTIVE

    return grid


def _print(grid):
    for z in grid:
        print(np.matrix(z))


def _pt1(grid):
    nextstate = _game_of_life(grid)
    return sum(sum(r.count(ACTIVE) for r in z) for z in nextstate)


def main():
    parse = lambda l: [[[MAPPING[s] for s in r] for r in l]]
    t1 = parse(TEST.splitlines())
    g = parse(input_lines())
    return _pt1(t1), _pt1(g)