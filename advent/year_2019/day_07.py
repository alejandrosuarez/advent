"""
"""

from advent.tools import *


def _pt1(lines):
    print(lines)


def _pt2(lines):
    pass


TEST1 = "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"
TEST2 = "3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0"
TEST3 = "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0"


def main():
    return afs.input_lines(
        tests=[TEST1, TEST2, TEST3],
        parts=[_pt1],
        run_input=False,
        transform_lines=lambda l: l[0].split(","),
        transform_line=int,
    )
