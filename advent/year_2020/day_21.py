"""
--- Day 21: Allergen Assessment ---
You reach the train's last stop and the closest you can get to your vacation island without getting wet.
There aren't even any boats here, but nothing can stop you now: you build a raft.
You just need a few days' worth of food for your journey.

You don't speak the local language, so you can't read any ingredients lists. However, sometimes,
allergens are listed in a language you do understand. You should be able to use this information to
determine which ingredient contains which allergen and work out which foods are safe to take with you on your trip.

You start by compiling a list of foods (your puzzle input), one food per line. Each line includes that
food's ingredients list followed by some or all of the allergens the food contains.

Each allergen is found in exactly one ingredient. Each ingredient contains zero or one allergen.
Allergens aren't always marked; when they're listed (as in (contains nuts, shellfish) after an ingredients list),
the ingredient that contains each listed allergen will be somewhere in the corresponding ingredients list.
However, even if an allergen isn't listed, the ingredient that contains that allergen could still be present:
maybe they forgot to label it, or maybe it was labeled in a language you don't know.

For example, consider the following list of foods:

mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
The first food in the list has four ingredients (written in a language you don't understand):
mxmxvkd, kfcds, sqjhc, and nhms. While the food might contain other allergens, a few allergens
the food definitely contains are listed afterward: dairy and fish.

The first step is to determine which ingredients can't possibly contain any of the allergens in any food in your list.
In the above example, none of the ingredients kfcds, nhms, sbzzf, or trh can contain an allergen.
Counting the number of times any of these ingredients appear in any ingredients list produces 5:
they all appear once each except sbzzf, which appears twice.

Determine which ingredients cannot possibly contain any of the allergens in your list.
How many times do any of those ingredients appear?

Your puzzle answer was 2436.

--- Part Two ---
Now that you've isolated the inert ingredients, you should have enough information to figure out
which ingredient contains which allergen.

In the above example:

mxmxvkd contains dairy.
sqjhc contains fish.
fvjkl contains soy.
Arrange the ingredients alphabetically by their allergen and separate them by commas to
produce your canonical dangerous ingredient list. (There should not be any spaces in your canonical
dangerous ingredient list.) In the above example, this would be mxmxvkd,sqjhc,fvjkl.

Time to stock your raft with supplies. What is your canonical dangerous ingredient list?

Your puzzle answer was dhfng,pgblcd,xhkdc,ghlzj,dstct,nqbnmzx,ntggc,znrzgs.

Both parts of this puzzle are complete! They provide two gold stars: **
"""

from advent.tools import *
from advent.util import input_lines
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import maximum_bipartite_matching as match


def _parse(lines):
    inp = [re.sub(r" \(|\)", "", l).split("contains ") for l in lines]
    return [[set(ing.split(" ")), set(alg.split(", "))] for ing, alg in inp]


def _build_matrix(lists):
    allergens = set(np.concatenate([list(a) for _, a in lists]))
    ingredients = set(np.concatenate([list(i) for i, _ in lists]))
    valid, invalid, counts = (
        cl.defaultdict(set),
        cl.defaultdict(set),
        cl.defaultdict(int),
    )

    for ing, alg in lists:
        for i in ing:
            counts[i] += 1

        for a in alg:
            valid[a] |= ing
            invalid[a] |= ingredients - ing

    for k, v in invalid.items():
        valid[k] -= v

    return ingredients, allergens, counts, valid


def _pt2(lists):
    ingredients, allergens, counts, valid = _build_matrix(lists)
    imap = {j: i for j, i in enumerate(ingredients)}
    amap = {j: i for j, i in enumerate(allergens)}
    mtx = np.zeros(shape=(len(imap), len(amap)), dtype=np.int8)

    for i, ing in imap.items():
        for j, alg in amap.items():
            if ing in valid[alg]:
                mtx[i][j] = 1

    assignments = {imap[j]: amap[i] for i, j in enumerate(match(csr_matrix(mtx)))}
    pairs = sorted(list(assignments.items()), key=lambda a: a[1])
    return ",".join(i for i, _ in pairs)


def _pt1(lists):
    ingredients, _, counts, valid = _build_matrix(lists)
    unsafe = ft.reduce(lambda x, y: x | y, valid.values(), set())
    safe = ingredients - unsafe

    return sum(counts[s] for s in safe)


TEST = """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)"""


def main():
    t = _parse(TEST.splitlines())
    s = _parse(input_lines())

    return _pt1(t), _pt1(s), _pt2(t), _pt2(s)