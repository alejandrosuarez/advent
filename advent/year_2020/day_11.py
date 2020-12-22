"""
--- Day 11: Seating System ---
Your plane lands with plenty of time to spare. The final leg of your journey is a ferry that goes directly
to the tropical island where you can finally start your vacation. As you reach the waiting area to board the ferry,
you realize you're so early, nobody else has even arrived yet!

By modeling the process people use to choose (or abandon) their seat in the waiting area,
you're pretty sure you can predict the best place to sit. You make a quick map of the seat layout (your puzzle input).

The seat layout fits neatly on a grid. Each position is either floor (.), an empty seat (L),
or an occupied seat (#). For example, the initial seat layout might look like this:

L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
Now, you just need to model the people who will be arriving shortly. Fortunately, people are entirely predictable
and always follow a simple set of rules. All decisions are based on the number of occupied seats adjacent
to a given seat (one of the eight positions immediately up, down, left, right, or diagonal from the seat).
The following rules are applied to every seat simultaneously:

If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
Otherwise, the seat's state does not change.
Floor (.) never changes; seats don't move, and nobody sits on the floor.

After one round of these rules, every seat in the example layout becomes occupied:

#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##
After a second round, the seats with four or more occupied adjacent seats become empty again:

#.LL.L#.##
#LLLLLL.L#
L.L.L..L..
#LLL.LL.L#
#.LL.LL.LL
#.LLLL#.##
..L.L.....
#LLLLLLLL#
#.LLLLLL.L
#.#LLLL.##
This process continues for three more rounds:

#.##.L#.##
#L###LL.L#
L.#.#..#..
#L##.##.L#
#.##.LL.LL
#.###L#.##
..#.#.....
#L######L#
#.LL###L.L
#.#L###.##
#.#L.L#.##
#LLL#LL.L#
L.L.L..#..
#LLL.##.L#
#.LL.LL.LL
#.LL#L#.##
..L.L.....
#L#LLLL#L#
#.LLLLLL.L
#.#L#L#.##
#.#L.L#.##
#LLL#LL.L#
L.#.L..#..
#L##.##.L#
#.#L.LL.LL
#.#L#L#.##
..L.L.....
#L#L##L#L#
#.LLLLLL.L
#.#L#L#.##
At this point, something interesting happens: the chaos stabilizes and further applications of these rules cause
no seats to change state! Once people stop moving around, you count 37 occupied seats.

Simulate your seating area by applying the seating rules repeatedly until no seats change state.
How many seats end up occupied?

Your puzzle answer was 2296.

--- Part Two ---
As soon as people start to arrive, you realize your mistake. People don't just care about adjacent seats -
they care about the first seat they can see in each of those eight directions!

Now, instead of considering just the eight immediately adjacent seats, consider the first seat in each of
those eight directions. For example, the empty seat below would see eight occupied seats:

.......#.
...#.....
.#.......
.........
..#L....#
....#....
.........
#........
...#.....
The leftmost empty seat below would only see one empty seat, but cannot see any of the occupied ones:

.............
.L.L.#.#.#.#.
.............
The empty seat below would see no occupied seats:

.##.##.
#.#.#.#
##...##
...L...
##...##
#.#.#.#
.##.##.
Also, people seem to be more tolerant than you expected: it now takes five or more visible occupied seats
for an occupied seat to become empty (rather than four or more from the previous rules).
The other rules still apply: empty seats that see no occupied seats become occupied, seats matching no
rule don't change, and floor never changes.

Given the same starting layout as above, these new rules cause the seating area to shift around as follows:

L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##
#.LL.LL.L#
#LLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLL#
#.LLLLLL.L
#.LLLLL.L#
#.L#.##.L#
#L#####.LL
L.#.#..#..
##L#.##.##
#.##.#L.##
#.#####.#L
..#.#.....
LLL####LL#
#.L#####.L
#.L####.L#
#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##LL.LL.L#
L.LL.LL.L#
#.LLLLL.LL
..L.L.....
LLLLLLLLL#
#.LLLLL#.L
#.L#LL#.L#
#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##L#.#L.L#
L.L#.#L.L#
#.L####.LL
..#.#.....
LLL###LLL#
#.LLLLL#.L
#.L#LL#.L#
#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##L#.#L.L#
L.L#.LL.L#
#.LLLL#.LL
..#.L.....
LLL###LLL#
#.LLLLL#.L
#.L#LL#.L#
Again, at this point, people stop shifting around and the seating area reaches equilibrium.
Once this occurs, you count 26 occupied seats.

Given the new visibility method and the rule change for occupied seats becoming empty, once equilibrium is reached,
how many seats end up occupied?

Your puzzle answer was 2089.

Both parts of this puzzle are complete! They provide two gold stars: **
"""

from advent.tools import *

FLOOR, EMPTY, OCCUPIED = 0, 1, 2
MAPPING = {".": FLOOR, "L": EMPTY, "#": OCCUPIED}
DIRS = [(1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1)]


def _game_of_life(grid, neighbors, tolerance):
    m, n, changed = len(grid), len(grid[0]), True

    while changed:
        changed = False

        for r in range(m):
            for c in range(n):
                grid[r][c][0] = grid[r][c][1]

        for r in range(m):
            for c in range(n):
                adj = len(list(neighbors(grid, r, c)))

                if grid[r][c][0] == EMPTY and adj == 0:
                    grid[r][c][1], changed = OCCUPIED, True
                elif grid[r][c][0] == OCCUPIED and adj >= tolerance:
                    grid[r][c][1], changed = EMPTY, True

    return sum([c for _, c in r].count(OCCUPIED) for r in grid)


def _pt1(grid):
    m, n = len(grid), len(grid[0])

    def neighbors(g, r, c):
        for y, x in DIRS:
            nr, nc = r + y, c + x
            if 0 <= nr < m and 0 <= nc < n:
                if grid[nr][nc][0] == OCCUPIED:
                    yield nr, nc

    return _game_of_life(grid, neighbors, 4)


def _pt2(grid):
    m, n = len(grid), len(grid[0])

    def neighbors(g, r, c):
        for y, x in DIRS:
            nr, nc = r, c

            while True:
                nr, nc = nr + y, nc + x

                if 0 <= nr < m and 0 <= nc < n:
                    if g[nr][nc][0] == FLOOR:
                        continue
                    else:
                        if g[nr][nc][0] == OCCUPIED:
                            yield nr, nc
                        break
                else:
                    break

    return _game_of_life(grid, neighbors, 5)


def main():
    grid = [[[None, MAPPING[s]] for s in r] for r in afs.input_lines()]
    pt1 = _pt1(cp.deepcopy(grid))
    pt2 = _pt2(cp.deepcopy(grid))

    return pt1, pt2