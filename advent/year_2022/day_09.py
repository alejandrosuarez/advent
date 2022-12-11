"""
"""

from advent.tools import *


def _pt1(lines):
    pass


def _pt2(lines):
    pass


TEST = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
"""
TEST2 = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
"""
ANSWERS = None


def main():
    return afs.input_lines(
        tests=[TEST],
        parts=[_pt1, _pt2],
        # run_input=False,
        transform_line=lambda l: (l.split(" ")[0], int(l.split(" ")[1])),
    )
