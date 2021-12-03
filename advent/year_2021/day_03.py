"""
"""

from advent.tools import *


def _pt1(lines):
    bit_count = len(lines[0])
    gamma = [0 for _ in range(bit_count)]
    epsilon = [0 for _ in range(bit_count)]

    for bit in range(bit_count):
        counts = [0, 0]

        for line in lines:
            counts[line[bit]] += 1

        gamma[bit] = counts.index(max(counts))
        epsilon[bit] = counts.index(min(counts))

    gamma_int = int("".join(map(str, gamma)), 2)
    epsilon_int = int("".join(map(str, epsilon)), 2)

    return gamma_int * epsilon_int


def _pt2(lines):
    pass


TEST = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
"""
ANSWERS = [198, 845186]


def main():
    return afs.input_lines(
        tests=[TEST],
        parts=[_pt1],
        run_input=True,
        transform_line=lambda l: list(map(int, list(l))),
    )
