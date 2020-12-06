"""
fuel = mass // 3 - 2
"""

from advent.util import load_input


def _calc_fuel(m):
    m, s = int(m.strip()), 0

    while m > 0:
        f = m // 3 - 2
        if f <= 0:
            break
        m, s = f, s + f

    return s


def main():
    pt1 = sum(int(m.strip()) // 3 - 2 for m in load_input())
    pt2 = sum(_calc_fuel(m) for m in load_input())

    return pt1, pt2