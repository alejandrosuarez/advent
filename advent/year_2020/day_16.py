"""
--- Day 16: Ticket Translation ---
As you're walking to yet another connecting flight, you realize that one of the legs of your
re-routed trip coming up is on a high-speed train. However, the train ticket you were given is in a
language you don't understand. You should probably figure out what it says before you get to the train
station after the next flight.

Unfortunately, you can't actually read the words on the ticket. You can, however, read the numbers,
and so you figure out the fields these tickets must have and the valid ranges for values in those fields.

You collect the rules for ticket fields, the numbers on your ticket, and the numbers on other nearby
tickets for the same train service (via the airport security cameras) together into a single document
you can reference (your puzzle input).

The rules for ticket fields specify a list of fields that exist somewhere on the ticket and the valid
ranges of values for each field. For example, a rule like class: 1-3 or 5-7 means that one of the
fields in every ticket is named class and can be any value in the ranges 1-3 or 5-7 (inclusive,
such that 3 and 5 are both valid in this field, but 4 is not).

Each ticket is represented by a single line of comma-separated values. The values are the numbers on the
ticket in the order they appear; every ticket has the same format. For example, consider this ticket:

.--------------------------------------------------------.
| ????: 101    ?????: 102   ??????????: 103     ???: 104 |
|                                                        |
| ??: 301  ??: 302             ???????: 303      ??????? |
| ??: 401  ??: 402           ???? ????: 403    ????????? |
'--------------------------------------------------------'
Here, ? represents text in a language you don't understand. This ticket might be represented as
101,102,103,104,301,302,303,401,402,403; of course, the actual train tickets you're looking at are
much more complicated. In any case, you've extracted just the numbers in such a way that the first
number is always the same specific field, the second number is always a different specific field,
and so on - you just don't know what each position actually means!

Start by determining which tickets are completely invalid; these are tickets that contain values which
aren't valid for any field. Ignore your ticket for now.

For example, suppose you have the following notes:

class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
It doesn't matter which position corresponds to which field; you can identify invalid nearby tickets
by considering only whether tickets contain values that are not valid for any field. In this example,
the values on the first nearby ticket are all valid for at least one field. This is not true of the other
three nearby tickets: the values 4, 55, and 12 are are not valid for any field. Adding together all of the
invalid values produces your ticket scanning error rate: 4 + 55 + 12 = 71.

Consider the validity of the nearby tickets you scanned. What is your ticket scanning error rate?

Your puzzle answer was 27802.

--- Part Two ---
Now that you've identified which tickets contain invalid values, discard those tickets entirely.
Use the remaining valid tickets to determine which field is which.

Using the valid ranges for each field, determine what order the fields appear on the tickets.
The order is consistent between all tickets: if seat is the third field, it is the third field on every
ticket, including your ticket.

For example, suppose you have the following notes:

class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9
Based on the nearby tickets in the above example, the first position must be row, the second position
must be class, and the third position must be seat; you can conclude that in your ticket, 
lass is 12, row is 11, and seat is 13.

Once you work out which field is which, look for the six fields on your ticket that start with the
word departure. What do you get if you multiply those six values together?

Your puzzle answer was 279139880759.

Both parts of this puzzle are complete! They provide two gold stars: **

knowledge
- a column must be assigned to a field name
- if a column is assigned to a field name, it cannot be assigned
to another field name
- if a field name is assigned to a column, it cannot be assigned
to another column
- in our map
    - a column cannot be assigned to any field names not in the
    adjacency list

assign columns to field names
build map of col # to possible field names based on overlap

{
    0: {"row"},
    1: {"row", "class"},
    2: {"row", "seat", "class"},
}

build logic using this graph
sat solve to assign cols to field names
"""

from advent.tools import *
from pysat.solvers import Maplesat as Solver

START, END, QUERY = 0, 2, 1


def _sweep(ranges, nearby):
    events = []

    for start, end, field in ranges:
        events.append((start, START, field))
        events.append((end, END, field))

    for val, col in nearby:
        events.append((val, QUERY, col))

    events.sort(key=lambda e: e[:2])
    active = set()

    for val, event, data in events:
        if event == START:
            active.add(data)
        elif event == END:
            active.remove(data)
        else:
            yield val, data, active


def _pt1(args):
    r, _, n = args
    return sum(v for v, _, z in _sweep(r, n) if not z)


class Logic:
    def __init__(self, cols, fields, graph):
        self.cols = cols
        self.fields = fields
        self.graph = graph
        self.sat = Solver(bootstrap_with=self.cnf)

    def term(self, field, col):
        fields_to_int = {f: i + len(self.cols) for i, f in enumerate(self.fields)}
        fi = fields_to_int[field]
        return fi * len(self.cols) + col + 1

    @property
    def cnf(self):
        cnf = []
        fields, cols, term = self.fields, self.cols, self.term

        # column can only be assigned to 1 field name
        for c in cols:
            for a, b in it.combinations(fields, 2):
                cnf.append([-term(a, c), -term(b, c)])

        # field name can only be assigned to 1 column
        for f in fields:
            for a, b in it.combinations(cols, 2):
                cnf.append([-term(f, a), -term(f, b)])

        # knowledge from sweep line
        for c in cols:
            d = []
            for f in fields:
                if f not in self.graph[c]:
                    cnf.append([-term(f, c)])
                else:
                    d.append(term(f, c))
            cnf.append(d)

        return cnf

    def test(self, field, col):
        trm = self.term(field, col)
        a = self.sat.solve(assumptions=[trm])
        if not a:
            return a
        b = self.sat.solve(assumptions=[-trm])
        if not b:
            return a
        return None


def _pt2(args):
    r, t, n = args
    cols = {x for x in range(len(t))}
    fields = {x for _, _, x in r}
    graph = {x: fields.copy() for x in cols}

    for val, col, active in _sweep(r, n):
        if active:
            graph[col] &= active

    logic = Logic(cols, fields, graph)
    assignments = [0] * len(cols)

    for c in cols:
        for f in fields:
            if logic.test(f, c):
                assignments[c] = f

    mapped = list(zip(assignments, t))

    return math.prod(v for k, v in mapped if k.startswith("departure"))


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


def _transform(groups):
    ranges, ticket, notes = groups
    range_grps = ranges.splitlines()
    ranges, nearby = [], []
    ticket = list(map(int, ticket.splitlines()[1].split(",")))

    for g in range_grps:
        field = re.match(r"^(.*):", g).groups()[0]
        ranges += [(int(s), int(e), field) for s, e in re.findall(r"(\d+)-(\d+)", g)]

    for row in notes.splitlines()[1:]:
        for col, val in enumerate(row.split(",")):
            nearby.append((int(val), col))

    return ranges, ticket, nearby


def main():
    return afs.input_groups(
        tests=[TEST1, TEST2],
        transform_groups=_transform,
        parts=[_pt1, _pt2],
    )