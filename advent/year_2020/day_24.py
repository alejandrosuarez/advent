"""
--- Day 24: Lobby Layout ---
Your raft makes it to the tropical island; it turns out that the small crab was an excellent navigator.
You make your way to the resort.

As you enter the lobby, you discover a small problem: the floor is being renovated.
You can't even reach the check-in desk until they've finished installing the new tile floor.

The tiles are all hexagonal; they need to be arranged in a hex grid with a very specific color pattern.
Not in the mood to wait, you offer to help figure out the pattern.

The tiles are all white on one side and black on the other. They start with the white side facing up.
The lobby is large enough to fit whatever pattern might need to appear there.

A member of the renovation crew gives you a list of the tiles that need to be flipped over (your puzzle input).
Each line in the list identifies a single tile that needs to be flipped by giving a series of steps starting from a
reference tile in the very center of the room. (Every line starts from the same reference tile.)

Because the tiles are hexagonal, every tile has six neighbors: east, southeast, southwest, west, northwest, and northeast.
These directions are given in your list, respectively, as e, se, sw, w, nw, and ne.
A tile is identified by a series of these directions with no delimiters; for example, esenee identifies the
tile you land on if you start at the reference tile and then move one tile east, one tile southeast, one tile northeast,
and one tile east.

Each time a tile is identified, it flips from white to black or from black to white. Tiles might be flipped more than once.
For example, a line like esew flips a tile immediately adjacent to the reference tile, and a line like nwwswee flips the
reference tile itself.

Here is a larger example:

sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew
In the above example, 10 tiles are flipped once (to black), and 5 more are flipped twice (to black, then back to white).
After all of these instructions have been followed, a total of 10 tiles are black.

Go through the renovation crew's list and determine which tiles they need to flip. After all of the instructions have been followed,
how many tiles are left with the black side up?

Your puzzle answer was 330.

--- Part Two ---
The tile floor in the lobby is meant to be a living art exhibit. Every day, the tiles are all flipped according to the following rules:

Any black tile with zero or more than 2 black tiles immediately adjacent to it is flipped to white.
Any white tile with exactly 2 black tiles immediately adjacent to it is flipped to black.
Here, tiles immediately adjacent means the six tiles directly touching the tile in question.

The rules are applied simultaneously to every tile; put another way, it is first determined which tiles need to be
flipped, then they are all flipped at the same time.

In the above example, the number of black tiles that are facing up after the given number of days has passed is as follows:

Day 1: 15
Day 2: 12
Day 3: 25
Day 4: 14
Day 5: 23
Day 6: 28
Day 7: 41
Day 8: 37
Day 9: 49
Day 10: 37

Day 20: 132
Day 30: 259
Day 40: 406
Day 50: 566
Day 60: 788
Day 70: 1106
Day 80: 1373
Day 90: 1844
Day 100: 2208
After executing this process a total of 100 times, there would be 2208 black tiles facing up.

How many tiles will be black after 100 days?

Your puzzle answer was 3711.

Both parts of this puzzle are complete! They provide two gold stars: **
"""

from advent.tools import *

DIRS = {
    "e": (1.0, 0),
    "se": (0.5, 1),
    "sw": (-0.5, 1),
    "w": (-1, 0),
    "nw": (-0.5, -1),
    "ne": (0.5, -1),
}


def _follow_directions(path):
    x = y = 0

    for step in path:
        d = DIRS[step]
        x, y = x + d[0], y + d[1]

    return x, y


def _starting(tiles):
    colors = cl.defaultdict(int)

    for dirs in tiles:
        x, y = _follow_directions(dirs)
        colors[(x, y)] ^= 1

    return colors


def _game_of_life(colors, n=100):
    for _ in range(n):
        last = cp.deepcopy(colors)
        neighbors = cl.defaultdict(int)

        for (x, y), color in last.items():
            if not color:
                continue

            for nx, ny in DIRS.values():
                neighbors[(x + nx, y + ny)] += 1

        universe = set(neighbors.keys()) | set(colors.keys())

        for coords in universe:
            count = neighbors[coords]

            if last[coords]:
                colors[coords] = not (count == 0 or count > 2)
            else:
                colors[coords] = count == 2

    return colors


def _pt1(tiles):
    return sum(_starting(tiles).values())


def _pt2(tiles):
    starting = _starting(tiles)
    colors = _game_of_life(starting)

    return sum(colors.values())


TEST1 = """esenee
nwwswee"""

TEST2 = """sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew"""


def _transform(line):
    p = "|".join(DIRS.keys())
    return re.findall(rf"{p}", line)


def main():
    return afs.input_lines(
        tests=[TEST1, TEST2],
        parts=[_pt1, _pt2],
        transform_line=_transform,
    )
