"""
--- Day 18: Operation Order ---
As you look out the window and notice a heavily-forested continent slowly appear over the horizon,
you are interrupted by the child sitting next to you. They're curious if you could help them with
their math homework.

Unfortunately, it seems like this "math" follows different rules than you remember.

The homework (your puzzle input) consists of a series of expressions that consist of addition (+),
multiplication (*), and parentheses ((...)). Just like normal math, parentheses indicate that the
expression inside must be evaluated before it can be used by the surrounding expression.
Addition still finds the sum of the numbers on both sides of the operator, and multiplication
still finds the product.

However, the rules of operator precedence have changed. Rather than evaluating multiplication before
addition, the operators have the same precedence, and are evaluated left-to-right regardless of the
order in which they appear.

For example, the steps to evaluate the expression 1 + 2 * 3 + 4 * 5 + 6 are as follows:

1 + 2 * 3 + 4 * 5 + 6
  3   * 3 + 4 * 5 + 6
      9   + 4 * 5 + 6
         13   * 5 + 6
             65   + 6
                 71
Parentheses can override this order; for example, here is what happens if parentheses are added to
form 1 + (2 * 3) + (4 * (5 + 6)):

1 + (2 * 3) + (4 * (5 + 6))
1 +    6    + (4 * (5 + 6))
     7      + (4 * (5 + 6))
     7      + (4 *   11   )
     7      +     44
            51
Here are a few more examples:

2 * 3 + (4 * 5) becomes 26.
5 + (8 * 3 + 9 + 3 * 4 * 3) becomes 437.
5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) becomes 12240.
((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 becomes 13632.
Before you can help with the homework, you need to understand it yourself.
Evaluate the expression on each line of the homework; what is the sum of the resulting values?

Your puzzle answer was 701339185745.

--- Part Two ---
You manage to answer the child's questions and they finish part 1 of their homework,
but get stuck when they reach the next section: advanced math.

Now, addition and multiplication have different precedence levels, but they're not the ones
you're familiar with. Instead, addition is evaluated before multiplication.

For example, the steps to evaluate the expression 1 + 2 * 3 + 4 * 5 + 6 are now as follows:

1 + 2 * 3 + 4 * 5 + 6
  3   * 3 + 4 * 5 + 6
  3   *   7   * 5 + 6
  3   *   7   *  11
     21       *  11
         231
Here are the other examples from above:

1 + (2 * 3) + (4 * (5 + 6)) still becomes 51.
2 * 3 + (4 * 5) becomes 46.
5 + (8 * 3 + 9 + 3 * 4 * 3) becomes 1445.
5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) becomes 669060.
((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 becomes 23340.
What do you get if you add up the results of evaluating the homework problems using these new rules?

Your puzzle answer was 4208490449905.

Both parts of this puzzle are complete! They provide two gold stars: **
"""

from re import sub
from collections import deque
from math import prod
from advent.util import input_lines

TEST1 = """1 + 2 * 3 + 4 * 5 + 6
1 + (2 * 3) + (4 * (5 + 6))
2 * 3 + (4 * 5)
5 + (8 * 3 + 9 + 3 * 4 * 3)
5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))
((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"""

TEST2 = """1 + 2 * 3 + 4 * 5 + 6
1 + (2 * 3) + (4 * (5 + 6))
2 * 3 + (4 * 5)
5 + (8 * 3 + 9 + 3 * 4 * 3)
5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))
((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2
"""


def _basic(expr):
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


def _advanced(expr):
    term, op = [[0]], ["+"]
    q = deque(list(expr))

    while q:
        tok = q.popleft()

        if tok in "+*":
            op[-1] = tok
        elif tok == "(":
            op.append("+")
            term.append([0])
        elif tok == ")":
            op.pop()
            q.appendleft(str(prod(term.pop())))
        elif op[-1] == "+":
            term[-1].append(int(tok) + term[-1].pop())
        elif op[-1] == "*":
            term[-1].append(int(tok))

    return prod(term[0])


def _pt1(exprs):
    return sum(map(_basic, exprs))


def _pt2(exprs):
    return sum(map(_advanced, exprs))


def main():
    parse = lambda s: [sub(r"\s+", "", l) for l in s]
    t1, t2 = parse(TEST1.splitlines()), parse(TEST2.splitlines())
    e = parse(input_lines())

    return _pt1(t1), _pt1(e), _pt2(t2), _pt2(e)