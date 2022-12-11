"""
"""

from advent.tools import *


def _pt1(lines):
    x = y = 0
    tx = ty = 0
    seen = set()
    grid = np.chararray((10, 10), unicode=True)
    grid[:] = "."

    def printgrid(grid):
        for row in grid:
            print("".join(row))

    def move(dist, dx, dy):
        nonlocal x, y, tx, ty
        for _ in range(dist):
            x += dx
            y += dy
            match (x - tx, y - ty):
                case (0, 0):
                    pass
                case (0, 2):
                    ty += 1
                case (0, -2):
                    ty -= 1
                case (2, 0):
                    tx += 1
                case (-2, 0):
                    tx -= 1
                case (2, 1):
                    tx += 1
                    ty += 1
                case (1, 2):
                    tx += 1
                    ty += 1
                case (-2, -1):
                    tx -= 1
                    ty -= 1
                case (-1, -2):
                    tx -= 1
                    ty -= 1
                case (-2, 1):
                    tx -= 1
                    ty += 1
                case (-1, 2):
                    tx -= 1
                    ty += 1
                case (2, -1):
                    tx += 1
                    ty -= 1
                case (1, -2):
                    tx += 1
                    ty -= 1

            t = (tx, ty)
            seen.add(t)

    for d, dist in lines:
        match d:
            case "R":
                move(dist, 1, 0)
            case "L":
                move(dist, -1, 0)
            case "U":
                move(dist, 0, 1)
            case "D":
                move(dist, 0, -1)

    return len(seen)


def _pt2(lines):
    pass


TEST = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
"""
TEST2 = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
"""
ANSWERS = None


def main():
    return afs.input_lines(
        tests=[TEST],
        parts=[_pt1, _pt2],
        # run_input=False,
        transform_line=lambda l: (l.split(" ")[0], int(l.split(" ")[1])),
    )
