"""
--- Day 20: Jurassic Jigsaw ---
The high-speed train leaves the forest and quickly carries you south.
You can even see a desert in the distance! Since you have some spare time, you might as well see
if there was anything interesting in the image the Mythical Information Bureau satellite captured.

After decoding the satellite messages, you discover that the data actually contains many small images
created by the satellite's camera array. The camera array consists of many cameras;
rather than produce a single square image, they produce many smaller square image tiles that need to
be reassembled back into a single image.

Each camera in the camera array returns a single monochrome image tile with a random unique ID number.
The tiles (your puzzle input) arrived in a random order.

Worse yet, the camera array appears to be malfunctioning: each image tile has been rotated and flipped to
a random orientation. Your first task is to reassemble the original image by orienting the tiles so they
fit together.

To show how the tiles should be reassembled, each tile's image data includes a border that should line
up exactly with its adjacent tiles. All tiles have this border, and the border lines up exactly when the
tiles are both oriented correctly. Tiles at the edge of the image also have this border, but the outermost
edges won't line up with any other tiles.

For example, suppose you have the following nine tiles:

Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...
By rotating, flipping, and rearranging them, you can find a square arrangement that causes all
adjacent borders to line up:

#...##.#.. ..###..### #.#.#####.
..#.#..#.# ###...#.#. .#..######
.###....#. ..#....#.. ..#.......
###.##.##. .#.#.#..## ######....
.###.##### ##...#.### ####.#..#.
.##.#....# ##.##.###. .#...#.##.
#...###### ####.#...# #.#####.##
.....#..## #...##..#. ..#.###...
#.####...# ##..#..... ..#.......
#.##...##. ..##.#..#. ..#.###...

#.##...##. ..##.#..#. ..#.###...
##..#.##.. ..#..###.# ##.##....#
##.####... .#.####.#. ..#.###..#
####.#.#.. ...#.##### ###.#..###
.#.####... ...##..##. .######.##
.##..##.#. ....#...## #.#.#.#...
....#..#.# #.#.#.##.# #.###.###.
..#.#..... .#.##.#..# #.###.##..
####.#.... .#..#.##.. .######...
...#.#.#.# ###.##.#.. .##...####

...#.#.#.# ###.##.#.. .##...####
..#.#.###. ..##.##.## #..#.##..#
..####.### ##.#...##. .#.#..#.##
#..#.#..#. ...#.#.#.. .####.###.
.#..####.# #..#.#.#.# ####.###..
.#####..## #####...#. .##....##.
##.##..#.. ..#...#... .####...#.
#.#.###... .##..##... .####.##.#
#...###... ..##...#.. ...#..####
..#.#....# ##.#.#.... ...##.....
For reference, the IDs of the above tiles are:

1951    2311    3079
2729    1427    2473
2971    1489    1171
To check that you've assembled the image correctly, multiply the IDs of the four corner tiles together.
If you do this with the assembled tiles from the example above,
you get 1951 * 3079 * 2971 * 1171 = 20899048083289.

Assemble the tiles into an image. What do you get if you multiply together the IDs of the four corner tiles?

Your puzzle answer was 15003787688423.

The first half of this puzzle is complete! It provides one gold star: *
"""

import numpy as np
import re
import itertools as it
import math
from collections import defaultdict, namedtuple
from dataclasses import dataclass
from typing import List, Tuple, Dict, Set
from advent.util import load_input

Rotation = namedtuple("Rotation", ["flip", "flip_axis", "rot", "pixels", "cropped"])


@dataclass
class Tile:
    id: int
    pixels: np.array

    def __post_init__(self):
        g = self.pixels
        borders = [g[0], g[-1], g[:, 0], g[:, -1]]
        self.border = list(map(tuple, borders))
        self.border += [e[::-1] for e in self.border]
        self.border = {b: i + 1 for i, b in enumerate(self.border)}

    @property
    def rotations(self):
        for r in range(4):
            rotated = np.rot90(self.pixels, r)
            cropped = np.rot90(self.cropped, r)
            yield Rotation(False, None, r, rotated, cropped)
            for f in range(2):
                yield Rotation(True, f, r, np.flip(rotated, f), np.flip(cropped, f))

    @property
    def cropped(self):
        return self.pixels[1:-1, 1:-1]


@dataclass
class Image:
    tiles: List[Tile]

    def __post_init__(self):
        self.graph, self.indegrees, self.shared = self._build_graph()
        self.placements = self._place_tiles()
        self.rot_instructions = self._rotate_tiles()

    def layout(self, cropped=False):
        rows = []

        for r in self.rot_instructions:
            row = []
            for c in r:
                row.append(c[-1 if cropped else -2])
            rows.append(row)

        return rows

    @property
    def tiles_index(self):
        return {t.id: t for t in self.tiles}

    @property
    def corners(self):
        return [t for t, i in self.indegrees.items() if i == 2]

    @property
    def borders(self):
        return [t for t, i in self.indegrees.items() if i == 3]

    def pixels(self, cropped=False):
        return np.vstack([np.hstack(r) for r in self.layout(cropped)])

    def pretty(self, cropped=True):
        return "\n".join(["".join(r) for r in self.pixels(cropped)])

    @property
    def rotations(self):
        for r in range(4):
            rotated = np.rot90(self.pixels(cropped=True), r)
            yield rotated
            for f in range(2):
                yield np.flip(rotated, f)

    @property
    def dimensions(self):
        b = len(self.borders)
        n = (b + 8) // 4
        return (n, n)

    def _rotate_tiles(self):
        """
        fix rotation of origin and its neighbors
        infer rotations for rest of grid row by row
        """

        p, s = self.placements, self.shared
        n = self.dimensions[0]
        rotations = [[None for _ in range(n)] for _ in range(n)]

        # figure out first 2 rotations
        origin, right, below = p[0][0], p[0][1], p[1][0]
        rshared, bshared = s[origin][right], s[origin][below]

        to, tr, tb = (
            self.tiles_index[origin],
            self.tiles_index[right],
            self.tiles_index[below],
        )

        # brute force top left corner
        def origin_rotations():
            for o in to.rotations:
                for b in tb.rotations:
                    for r in tr.rotations:
                        if (o.pixels[:, -1] == r.pixels[:, 0]).all() and (
                            o.pixels[-1] == b.pixels[0]
                        ).all():
                            return o, r, b

        orot, rrot, brot = origin_rotations()
        rotations[0][0], rotations[0][1], rotations[1][0] = orot, rrot, brot

        # arrangements for top row
        for c in range(2, len(p[0])):
            prev = rotations[0][c - 1]

            for rot in self.tiles_index[p[0][c]].rotations:
                if (rot.pixels[:, 0] == prev.pixels[:, -1]).all():
                    rotations[0][c] = rot
                    break

        # arrangements for left column
        for r in range(1, len(p)):
            prev = rotations[r - 1][0]

            for rot in self.tiles_index[p[r][0]].rotations:
                if (rot.pixels[0] == prev.pixels[-1]).all():
                    rotations[r][0] = rot
                    break

        # arrangements for rest of grid, top left to bottom right
        for r in range(1, len(p)):
            for c in range(1, len(p[0])):
                above, left = rotations[r - 1][c], rotations[r][c - 1]

                for rot in self.tiles_index[p[r][c]].rotations:
                    if (rot.pixels[0] == above.pixels[-1]).all() and (
                        rot.pixels[:, 0] == left.pixels[:, -1]
                    ).all():
                        rotations[r][c] = rot
                        break

        return np.array(rotations, dtype=Rotation)

    def _place_tiles(self):
        """
        pick a corner, assign as origin (top left)
        pick a neighbor of origin, assign that as next right neighbor
        on x axis. from there, go row-by-row and infer placements based on
        neighbors we've seen before and those we havent
        """

        n = self.dimensions[0]
        ind, graph = self.indegrees, self.graph
        layout = [[None for _ in range(n)] for _ in range(n)]
        origin = self.corners[0]
        nei = list(graph[origin])[1]
        layout[0][:2] = origin, nei
        seen = {origin, nei}

        for i in range(2, n):
            p = layout[0][i - 1]
            nei = next(t for t in graph[p] if ind[t] < 4 and t not in seen)
            layout[0][i] = nei
            seen.add(nei)

        for r in range(1, n):
            for c in range(n):
                a = layout[r - 1][c]
                tile = next(t for t in graph[a] if t not in seen)
                layout[r][c] = tile
                seen.add(tile)

        return np.array(layout)

    def _build_graph(self):
        index, graph, indegrees = (
            defaultdict(set),
            defaultdict(set),
            defaultdict(int),
        )

        for t in self.tiles:
            for b in t.border.keys():
                index[b].add(t.id)

        shared = defaultdict(dict)

        for border, tiles in index.items():
            for u, v in it.combinations(tiles, 2):
                indegrees[v] += v not in graph[u]
                indegrees[u] += u not in graph[v]
                graph[u].add(v)
                graph[v].add(u)
                shared[u][v] = border
                shared[v][u] = border

        return graph, indegrees, shared


def _parse(s):
    tiles = []

    for t in s.split("\n\n"):
        t = t.splitlines()
        g = [list(r) for r in t[1:]]
        t = int(re.match(r"^Tile (\d+):", t[0]).groups()[0])
        tiles.append(Tile(id=t, pixels=np.array(g)))

    return tiles


def _find_sms(img, sm_shape):
    for i, row in enumerate(img):
        for j, c in enumerate(row):
            try:
                if all(img[i + di][j + dj] == "#" for di, dj in sm_shape):
                    yield i, j
            except IndexError:
                continue


def _pt2(tiles):
    image = Image(tiles)

    sm_shape = [
        (r, c)
        for r, row in enumerate(SEA_MONSTER.splitlines())
        for c, p in enumerate(row)
        if p == "#"
    ]

    f = [(i, list(_find_sms(i, sm_shape))) for i in image.rotations]
    f = [(t, sm) for t, sm in f if sm]
    i, sms = f[0]
    sms = {(i + di, j + dj) for i, j in sms for di, dj in sm_shape}
    return sum(1 for (y, x), t in np.ndenumerate(i) if (y, x) not in sms and t == "#")


def _pt1(tiles):
    image = Image(tiles)

    return math.prod(image.corners)


TEST1 = """Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###..."""

TEST_EXPECTED_ARRANGEMENT = """.#.#..#.##...#.##..#####
###....#.#....#..#......
##.##.###.#.#..######...
###.#####...#.#####.#..#
##.#....#.##.####...#.##
...########.#....#####.#
....#..#...##..#.#.###..
.####...#..#.....#......
#..#.##..#..###.#.##....
#.####..#.####.#.#.###..
###.#.#...#.######.#..##
#.####....##..########.#
##..##.#...#...#.#.#.#..
...#..#..#.#.##..###.###
.#.#....#.##.#...###.##.
###.#...#..#.##.######..
.#.#.###.##.##.#..#.##..
.####.###.#...###.#..#.#
..#.#..#..#.#.#.####.###
#..####...#.#.#.###.###.
#####..#####...###....##
#.##..#..#...#..####...#
.#.###..##..##..####.##.
...###...##...#...#..###"""

SEA_MONSTER = """                  # 
#    ##    ##    ###
 #  #  #  #  #  #"""


def main():
    t = _parse(TEST1)
    s = _parse(load_input().read())
    return _pt1(t), _pt1(s), _pt2(t), _pt2(s)