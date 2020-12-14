"""
"""


from re import match
from collections import defaultdict
from typing import NamedTuple, Tuple, List
from advent.util import load_input


class Instruction(NamedTuple):
    mask: str
    writes: List[Tuple[int, int]]


def pt1(s):
    instructions, state = _parse(s), defaultdict(int)

    for mask, writes in instructions:
        for addr, val in writes:
            val |= int(mask.replace("X", "0"), 2)
            val &= int(mask.replace("X", "1"), 2)
            state[addr] = val

    return sum(state.values())


def _parse(s):
    grps = s.split("mask")[1:]
    grps = [g.splitlines() for g in grps]

    for i, g in enumerate(grps):
        g[0] = match(r" = ([01X]+)", g[0]).groups()[0]

        for j in range(1, len(g)):
            g[j] = match(r"mem\[(\d+)\] = (\d+)", g[j]).groups()

        grps[i] = Instruction(mask=g[0], writes=[(int(x), int(y)) for x, y in g[1:]])

    return grps


def main():
    return pt1(load_input().read())