"""
--- Day 14: Extended Polymerization ---
The incredible pressures at this depth are starting to put a strain on your submarine. The submarine has polymerization equipment that would produce suitable materials to reinforce the submarine, and the nearby volcanically-active caves should even have the necessary input elements in sufficient quantities.

The submarine manual contains instructions for finding the optimal polymer formula; specifically, it offers a polymer template and a list of pair insertion rules (your puzzle input). You just need to work out what polymer would result after repeating the pair insertion process a few times.

For example:

NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
The first line is the polymer template - this is the starting point of the process.

The following section defines the pair insertion rules. A rule like AB -> C means that when elements A and B are immediately adjacent, element C should be inserted between them. These insertions all happen simultaneously.

So, starting with the polymer template NNCB, the first step simultaneously considers all three pairs:

The first pair (NN) matches the rule NN -> C, so element C is inserted between the first N and the second N.
The second pair (NC) matches the rule NC -> B, so element B is inserted between the N and the C.
The third pair (CB) matches the rule CB -> H, so element H is inserted between the C and the B.
Note that these pairs overlap: the second element of one pair is the first element of the next pair. Also, because all pairs are considered simultaneously, inserted elements are not considered to be part of a pair until the next step.

After the first step of this process, the polymer becomes NCNBCHB.

Here are the results of a few steps using the above rules:

Template:     NNCB
After step 1: NCNBCHB
After step 2: NBCCNBBBCBHCB
After step 3: NBBBCNCCNBBNBNBBCHBHHBCHB
After step 4: NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB
This polymer grows quickly. After step 5, it has length 97; After step 10, it has length 3073. After step 10, B occurs 1749 times, C occurs 298 times, H occurs 161 times, and N occurs 865 times; taking the quantity of the most common element (B, 1749) and subtracting the quantity of the least common element (H, 161) produces 1749 - 161 = 1588.

Apply 10 steps of pair insertion to the polymer template and find the most and least common elements in the result. What do you get if you take the quantity of the most common element and subtract the quantity of the least common element?

Your puzzle answer was 2587.

--- Part Two ---
The resulting polymer isn't nearly strong enough to reinforce the submarine. You'll need to run more steps of the pair insertion process; a total of 40 steps should do it.

In the above example, the most common element is B (occurring 2192039569602 times) and the least common element is H (occurring 3849876073 times); subtracting these produces 2188189693529.

Apply 40 steps of pair insertion to the polymer template and find the most and least common elements in the result. What do you get if you take the quantity of the most common element and subtract the quantity of the least common element?

Your puzzle answer was 3318837563123.

Both parts of this puzzle are complete! They provide two gold stars: **
"""

from advent.tools import *


def _pt1(groups):
    tmpl, rules = groups
    rules = {tuple(k): v for k, v in [r.split(" -> ") for r in rules.splitlines()]}
    tmpl = cl.deque(list(tmpl))
    for _ in range(10):
        nxt_tmpl = cl.deque()
        while tmpl:
            tok = tmpl.popleft()
            nxt_tmpl.append(tok)
            if not tmpl:
                break
            if insert := rules.get((tok, tmpl[0])):
                nxt_tmpl.append(insert)
        tmpl = nxt_tmpl
    counts = cl.Counter(tmpl)
    counts = sorted(list(counts.values()))
    return counts[-1] - counts[0]


def _pt2(groups):
    tmpl, rules = groups
    rules = {tuple(k): v for k, v in [r.split(" -> ") for r in rules.splitlines()]}
    counts = cl.defaultdict(int)
    for a, b in zip(tmpl, tmpl[1:]):
        counts[a, b] += 1
    for _ in range(40):
        nxt_counts = cl.defaultdict(int)
        for k, v in counts.items():
            nxt_counts[k[0], rules[k]] += v
            nxt_counts[rules[k], k[1]] += v
        counts = nxt_counts
    char_counts = cl.defaultdict(int)
    for k, v in counts.items():
        char_counts[k[0]] += v
    char_counts[tmpl[-1]] += 1
    char_counts = sorted(char_counts.values())
    return char_counts[-1] - char_counts[0]


TEST = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
"""
ANSWERS = [1588, 2587, 2188189693529, 3318837563123]


def main():
    return afs.input_groups(tests=[TEST], parts=[_pt1, _pt2], run_input=True)
