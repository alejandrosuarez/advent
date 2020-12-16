"""
"""

from typing import List, Tuple
from re import findall
from advent.util import load_input

TEST1 = """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12"""

TEST2 = """class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9"""

START, END, QUERY = 0, 2, 1


def _invalid(ranges: List[Tuple[int, int]], nearby: List[int]):
    events = []

    for s, e in ranges:
        events.append((s, START))
        events.append((e, END))

    for n in nearby:
        events.append((n, QUERY))

    events.sort()
    balance = 0
    result = []

    for ts, event in events:
        if event == START:
            balance += 1
        elif event == END:
            balance -= 1
        elif balance == 0:
            result.append(ts)

    return result


def _pt1(ranges: List[Tuple[int, int]], ticket: str, nearby: List[int]):
    return sum(_invalid(ranges, nearby))


def _parse(s):
    ranges, ticket, nearby = s.split("\n\n")
    ranges = [(int(s), int(e)) for s, e in findall(r"(\d+)-(\d+)", ranges)]
    nearby = list(map(int, findall(r"(\d+)", nearby)))
    return ranges, ticket, nearby


def main():
    t1 = _parse(TEST1)
    s1 = _parse(load_input().read())

    return _pt1(*t1), _pt1(*s1)
