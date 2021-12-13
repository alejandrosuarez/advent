"""
"""

from advent.tools import *


def _next_state(fish):
    for i in range(len(fish)):
        fish[i] -= 1

        if fish[i] < 0:
            fish[i] = 6
            fish.append(8)

    return fish


def _pt1(lines):
    fish = lines[0]
    n = 80

    for _ in range(n):
        fish = _next_state(fish)

    return len(fish)


def _pt2(lines):
    fish = lines[0]
    n = 256

    for _ in range(n):
        fish = _next_state(fish)

    return len(fish)


TEST = """3,4,3,1,2
"""
ANSWERS = [5934, 343441]


def _transform_line(line):
    return list(map(int, line.split(",")))


def main():
    return afs.input_lines(
        tests=[TEST],
        parts=[_pt1, _pt2],
        run_input=False,
        transform_line=_transform_line,
    )
