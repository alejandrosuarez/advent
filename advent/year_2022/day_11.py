"""
"""

from advent.tools import *


@dc.dataclass
class Monkey:
    items: cl.deque[int]
    id_: int
    op: str
    test: int
    if_true: int
    if_false: int

    def call_operation(self, old: int):
        return eval(self.op.replace("old", str(old)))


def _pt1(notes):
    monkeys = {}
    for note in notes:
        mid = int(note[0].split(" ")[1][:-1])
        monkeys[mid] = Monkey(
            items=cl.deque(int(i) for i in note[1].split(": ")[1].split(", ")),
            id_=mid,
            op=note[2].split("= ")[1],
            test=int(note[3].split(" ")[-1]),
            if_true=int(note[4].split(" ")[-1]),
            if_false=int(note[5].split(" ")[-1]),
        )


def _pt2(lines):
    pass


TEST = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""
ANSWERS = None


def main():
    return afs.input_groups(
        tests=[TEST],
        parts=[_pt1, _pt2],
        run_input=False,
        transform_group=lambda g: [l.strip() for l in g.splitlines()],
    )
