"""
--- Day 3: Perfectly Spherical Houses in a Vacuum ---
Santa is delivering presents to an infinite two-dimensional grid of houses.

He begins by delivering a present to the house at his starting location, and then an elf at the North Pole
calls him via radio and tells him where to move next. Moves are always exactly one house to the north (^),
south (v), east (>), or west (<). After each move, he delivers another present to the house at his new location.

However, the elf back at the north pole has had a little too much eggnog, and so his directions are a little off,
and Santa ends up visiting some houses more than once. How many houses receive at least one present?

For example:

> delivers presents to 2 houses: one at the starting location, and one to the east.
^>v< delivers presents to 4 houses in a square, including twice to the house at his starting/ending location.
^v^v^v^v^v delivers a bunch of presents to some very lucky children at only 2 houses.
Your puzzle answer was 2565.

--- Part Two ---
The next year, to speed up the process, Santa creates a robot version of himself,
Robo-Santa, to deliver presents with him.

Santa and Robo-Santa start at the same location (delivering two presents to the same starting house),
then take turns moving based on instructions from the elf, who is eggnoggedly reading from the same
script as the previous year.

This year, how many houses receive at least one present?

For example:

^v delivers presents to 3 houses, because Santa goes north, and then Robo-Santa goes south.
^>v< now delivers presents to 3 houses, and Santa and Robo-Santa end up back where they started.
^v^v^v^v^v now delivers presents to 11 houses, with Santa going one direction and Robo-Santa going the other.
Your puzzle answer was 2639.

Both parts of this puzzle are complete! They provide two gold stars: **
"""

from advent.tools import *


def _pt1(directions):
    x, y = 0, 0
    houses = set()

    for d in directions:
        if d == ">":
            x += 1
        if d == "v":
            y -= 1
        if d == "^":
            y += 1
        if d == "<":
            x -= 1
        houses.add((x, y))

    return len(houses)


def _pt2(directions):
    coords = [[0, 0], [0, 0]]
    houses = {(0, 0)}

    for i, d in enumerate(directions):
        which = i % 2

        if d == ">":
            coords[which][0] += 1
        if d == "v":
            coords[which][1] -= 1
        if d == "^":
            coords[which][1] += 1
        if d == "<":
            coords[which][0] -= 1

        houses.add(tuple(coords[which]))

    return len(houses)


TEST1 = "^>v<"
TEST2 = "^v^v^v^v^v"
TEST3 = "^v"

ANSWERS = [4, 2, 2, 2565, 3, 11, 3, 2639]


def main():
    return afs.input_lines(
        tests=[TEST1, TEST2, TEST3],
        parts=[_pt1, _pt2],
        transform_lines=lambda l: list(l[0]),
    )
