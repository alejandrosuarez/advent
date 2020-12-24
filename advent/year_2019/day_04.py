"""
--- Day 4: Secure Container ---
You arrive at the Venus fuel depot only to discover it's protected by a password.
The Elves had written the password on a sticky note, but someone threw it out.

However, they do remember a few key facts about the password:

It is a six-digit number.
The value is within the range given in your puzzle input.
Two adjacent digits are the same (like 22 in 122345).
Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).
Other than the range rule, the following are true:

111111 meets these criteria (double 11, never decreases).
223450 does not meet these criteria (decreasing pair of digits 50).
123789 does not meet these criteria (no double).
How many different passwords within the range given in your puzzle input meet these criteria?

Your puzzle answer was 1748.

--- Part Two ---
An Elf just remembered one more important detail: the two adjacent matching digits are not
part of a larger group of matching digits.

Given this additional criterion, but still ignoring the range rule, the following are now true:

112233 meets these criteria because the digits never decrease and all repeated digits are exactly two digits long.
123444 no longer meets the criteria (the repeated 44 is part of a larger group of 444).
111122 meets the criteria (even though 1 is repeated more than twice, it still contains a double 22).
How many different passwords within the range given in your puzzle input meet all of the criteria?

Your puzzle answer was 1180.

Both parts of this puzzle are complete! They provide two gold stars: **

At this point, you should return to your Advent calendar and try another puzzle.

Your puzzle input was 146810-612564.
"""

from advent.tools import *


def _matches(s):
    return all([all(x <= y for x, y in zip(s, s[1:])), len(s) == 6])


def _matches_pt1(s):
    consecutive = max(len(list(g)) for _, g in it.groupby(s)) >= 2
    return _matches(s) and consecutive


def _matches_pt2(s):
    consecutive = 2 in set(len(list(g)) for _, g in it.groupby(s))
    return _matches(s) and consecutive


def _pt1(nums):
    assert _matches_pt1("111111")
    assert not _matches_pt1("223450")
    assert not _matches_pt1("123789")

    lo, hi = nums[0], nums[1] + 1

    return sum(map(_matches_pt1, map(str, range(lo, hi))))


def _pt2(nums):
    assert _matches_pt2("112233")
    assert not _matches_pt2("123444")
    assert _matches_pt2("111122")

    lo, hi = nums[0], nums[1] + 1

    return sum(map(_matches_pt2, map(str, range(lo, hi))))


ANSWERS = [1748, 1180]


def main():
    return afs.input_lines(
        parts=[_pt1, _pt2],
        transform_lines=lambda l: l[0].split("-"),
        transform_line=int,
    )
