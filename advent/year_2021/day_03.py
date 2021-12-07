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
    bit_count = len(lines[0])
    ratings = [0, 0]
    reports = [cp.copy(lines), cp.copy(lines)]

    for rating in range(2):
        for bit in range(bit_count):
            counts = [0, 0]
            criteria = 0

            for line in reports[rating]:
                counts[line[bit]] += 1

            if rating == 0:  # oxygen
                criteria = (
                    1 if min(counts) == max(counts) else counts.index(max(counts))
                )
            elif rating == 1:  # co2
                criteria = (
                    0 if min(counts) == max(counts) else counts.index(min(counts))
                )
            else:
                raise ValueError(rating)

            reports[rating] = [num for num in reports[rating] if num[bit] == criteria]

            if len(reports[rating]) == 1:
                ratings[rating] = int("".join(map(str, reports[rating][0])), 2)
                break

    return math.prod(ratings)


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
ANSWERS = [198, 845186, 230, 4636702]


def main():
    return afs.input_lines(
        tests=[TEST],
        parts=[_pt1, _pt2],
        run_input=True,
        transform_line=lambda l: list(map(int, list(l))),
    )
