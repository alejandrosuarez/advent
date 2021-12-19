"""
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
