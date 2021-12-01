"""
--- Day 6: Probably a Fire Hazard ---
Because your neighbors keep defeating you in the holiday house decorating contest year after year,
you've decided to deploy one million lights in a 1000x1000 grid.

Furthermore, because you've been especially nice this year, Santa has mailed you instructions on how to display the
ideal lighting configuration.

Lights in your grid are numbered from 0 to 999 in each direction; the lights at each corner are at 0,0, 0,999, 999,999,
and 999,0. The instructions include whether to turn on, turn off, or toggle various inclusive ranges given as coordinate pairs.
Each coordinate pair represents opposite corners of a rectangle, inclusive; a coordinate pair like 0,0 through 2,2
therefore refers to 9 lights in a 3x3 square. The lights all start turned off.

To defeat your neighbors this year, all you have to do is set up your lights by doing the instructions Santa sent you in order.

For example:

turn on 0,0 through 999,999 would turn on (or leave on) every light.
toggle 0,0 through 999,0 would toggle the first line of 1000 lights, turning off the ones that were on,
and turning on the ones that were off.
turn off 499,499 through 500,500 would turn off (or leave off) the middle four lights.
After following the instructions, how many lights are lit?

Your puzzle answer was 543903.

The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---
You just finish implementing your winning light pattern when you realize you
mistranslated Santa's message from Ancient Nordic Elvish.

The light grid you bought actually has individual brightness controls;
each light can have a brightness of zero or more. The lights all start at zero.

The phrase turn on actually means that you should increase the brightness of those lights by 1.

The phrase turn off actually means that you should decrease the brightness of those lights by 1,
to a minimum of zero.

The phrase toggle actually means that you should increase the brightness of those lights by 2.

What is the total brightness of all lights combined after following Santa's instructions?

For example:

turn on 0,0 through 0,0 would increase the total brightness by 1.
toggle 0,0 through 999,999 would increase the total brightness by 2000000.
"""

from typing import NamedTuple, Tuple

from advent.tools import *


class Command(NamedTuple):
    instruction: str
    start: Tuple[int, int]
    end: Tuple[int, int]


def _parse(line):
    patt = r"^(turn on|toggle|turn off) (\d+),(\d+) through (\d+),(\d+)$"
    grps = re.match(patt, line).groups()

    return Command(
        grps[0],
        (int(grps[1]), int(grps[2])),
        (int(grps[3]) + 1, int(grps[4]) + 1),
    )


def _pt1(lines):
    size = 1000
    grid = [[0 for _ in range(size)] for _ in range(size)]

    for cmd in map(_parse, lines):
        for c in range(cmd.start[0], cmd.end[0]):
            for r in range(cmd.start[1], cmd.end[1]):
                if cmd.instruction == "toggle":
                    grid[r][c] ^= 1
                elif cmd.instruction == "turn off":
                    grid[r][c] = 0
                elif cmd.instruction == "turn on":
                    grid[r][c] = 1
                else:
                    raise ValueError(cmd.instruction)

    return sum(r.count(1) for r in grid)


def _pt2(lines):
    size = 1000
    grid = [[0 for _ in range(size)] for _ in range(size)]

    for cmd in map(_parse, lines):
        for c in range(cmd.start[0], cmd.end[0]):
            for r in range(cmd.start[1], cmd.end[1]):
                if cmd.instruction == "toggle":
                    grid[r][c] += 2
                elif cmd.instruction == "turn off":
                    grid[r][c] = max(0, grid[r][c] - 1)
                elif cmd.instruction == "turn on":
                    grid[r][c] += 1
                else:
                    raise ValueError(cmd.instruction)

    return sum(map(sum, grid))


ANSWERS = [543903, 14687245]


def main():
    return afs.input_lines(tests=[], parts=[_pt1, _pt2], run_input=True)
