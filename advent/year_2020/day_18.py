"""
"""

from re import sub
from collections import deque
from advent.util import input_lines

TEST = """1 + 2 * 3 + 4 * 5 + 6
1 + (2 * 3) + (4 * (5 + 6))
2 * 3 + (4 * 5)
5 + (8 * 3 + 9 + 3 * 4 * 3)
5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))
((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"""


def _eval(expr):
    term, op = [0], ["+"]
    q = deque(list(expr))

    while q:
        tok = q.popleft()

        if tok in "+*":
            op[-1] = tok
        elif tok == "(":
            op.append("+")
            term.append(0)
        elif tok == ")":
            op.pop()
            q.appendleft(str(term.pop()))
        elif op[-1] == "+":
            term[-1] += int(tok)
        elif op[-1] == "*":
            term[-1] *= int(tok)

    return term[0]


def _pt1(exprs):
    return sum(_eval(x) for x in exprs)


def main():
    parse = lambda s: [sub(r"\s+", "", l) for l in s]
    t = parse(TEST.splitlines())
    e = parse(input_lines())

    return _pt1(t), _pt1(e)