"""
"""

from advent.tools import *


def _scan(parens):
    bal = 0

    for tok in parens:
        if tok == "(":
            bal += 1
        else:
            bal -= 1
        yield bal


def _pt1(l):
    return list(_scan(l))[-1]


def _pt2(l):
    i = 0
    for bal in _scan(l):
        i += 1
        if bal < 0:
            return i


TEST = "()())"

ANSWERS = [-1, 138, 5, 1771]


def main():
    return afs.input_lines(
        tests=[TEST],
        parts=[_pt1, _pt2],
        transform_lines=lambda l: list(l[0]),
    )
