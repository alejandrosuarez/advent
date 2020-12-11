"""
floor (.), an empty seat (L), or an occupied seat (#)

"""

from collections import defaultdict
from advent.util import input_lines
from scipy.ndimage import convolve

FLOOR, EMPTY, OCCUPIED = 0, 1, 2
MAPPING = {".": FLOOR, "L": EMPTY, "#": OCCUPIED}


def _pt1(grid):
    last = None
    kernel = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
    m, n = len(grid), len(grid[0])

    while last != grid:
        last = [r[:] for r in grid]
        occ = [[1 if last[r][c] == OCCUPIED else 0 for c in range(n)] for r in range(m)]
        adj = convolve(occ, kernel, mode="constant")

        for r in range(m):
            for c in range(n):
                if adj[r][c] == 0 and last[r][c] == EMPTY:
                    grid[r][c] = OCCUPIED
                elif adj[r][c] >= 4 and last[r][c] == OCCUPIED:
                    grid[r][c] = EMPTY

    return sum(r.count(OCCUPIED) for r in grid)


def main():
    grid = [[MAPPING[s] for s in r] for r in input_lines()]
    pt1 = _pt1(grid)

    return pt1