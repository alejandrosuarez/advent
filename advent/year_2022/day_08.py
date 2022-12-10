"""
"""

from advent.tools import *


def annotate_coords(grid):
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            grid[r][c] = ((r, c), grid[r][c])


def _pt1(grid):
    grid = np.array(grid, dtype=object)
    rows, cols = len(grid), len(grid[0])
    annotate_coords(grid)
    coords = set()
    for _ in range(4):
        for r in range(1, rows - 1):
            rowmax = grid[r][0][1]
            for c in range(1, cols - 1):
                if grid[r][c][1] > rowmax:
                    coords.add(grid[r][c][0])
                rowmax = max(rowmax, grid[r][c][1])
        grid = np.rot90(grid)
    return len(coords) + (len(grid[0]) * 2) + (len(grid) * 2) - 4


def _pt2(grid):
    rows, cols = len(grid), len(grid[0])
    s = 0
    for r in range(rows):
        for c in range(cols):
            y = 1

            cur = 0
            for rr in range(r + 1, rows):
                cur += 1
                if grid[rr][c] >= grid[r][c]:
                    break
            y *= cur

            cur = 0
            for rr in range(r - 1, -1, -1):
                cur += 1
                if grid[rr][c] >= grid[r][c]:
                    break
            y *= cur

            cur = 0
            for rr in range(c + 1, cols):
                cur += 1
                if grid[r][rr] >= grid[r][c]:
                    break
            y *= cur

            cur = 0
            for rr in range(c - 1, -1, -1):
                cur += 1
                if grid[r][rr] >= grid[r][c]:
                    break
            y *= cur

            s = max(s, y)

    return s


TEST = """30373
25512
65332
33549
35390
"""
ANSWERS = None


def main():
    return afs.input_lines(
        tests=[TEST],
        parts=[_pt1, _pt2],
        # run_input=False,
        transform_line=lambda l: list(map(int, list(l))),
    )
