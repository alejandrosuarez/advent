"""
"""

from advent.util import input_lines


def pt1(lines):
    a, ids = _parse_lines(lines)
    ids = [(i, ((a // i) + 1) * i) for i in ids]
    i, d = min(ids, key=lambda i: i[1])
    return (d - a) * i


def _parse_lines(lines):
    a = int(lines[0])
    ids = [int(i) for i in lines[1].split(",") if i != "x"]
    return a, ids


def main():
    p1 = pt1(input_lines())

    return p1