"""
--- Day 12: Rain Risk ---
Your ferry made decent progress toward the island, but the storm came in faster than anyone expected. The ferry needs to take evasive actions!

Unfortunately, the ship's navigation computer seems to be malfunctioning; rather than giving a route directly to safety,
it produced extremely circuitous instructions. When the captain uses the PA system to ask if anyone can help, you quickly volunteer.

The navigation instructions (your puzzle input) consists of a sequence of single-character actions paired with integer input values.
After staring at them for a few minutes, you work out what they probably mean:

Action N means to move north by the given value.
Action S means to move south by the given value.
Action E means to move east by the given value.
Action W means to move west by the given value.
Action L means to turn left the given number of degrees.
Action R means to turn right the given number of degrees.
Action F means to move forward by the given value in the direction the ship is currently facing.
The ship starts by facing east. Only the L and R actions change the direction the ship is facing.
(That is, if the ship is facing east and the next instruction is N10, the ship would move north 10 units,
but would still move east if the following action were F.)

For example:

F10
N3
F7
R90
F11
These instructions would be handled as follows:

F10 would move the ship 10 units east (because the ship starts by facing east) to east 10, north 0.
N3 would move the ship 3 units north to east 10, north 3.
F7 would move the ship another 7 units east (because the ship is still facing east) to east 17, north 3.
R90 would cause the ship to turn right by 90 degrees and face south; it remains at east 17, north 3.
F11 would move the ship 11 units south to east 17, south 8.
At the end of these instructions, the ship's Manhattan distance (sum of the absolute values of its east/west position
and its north/south position) from its starting position is 17 + 8 = 25.

Figure out where the navigation instructions lead. What is the Manhattan distance between that location and the ship's starting position?

Your puzzle answer was 2847.

--- Part Two ---
Before you can give the destination to the captain, you realize that the actual action meanings were printed on the back of the instructions the whole time.

Almost all of the actions indicate how to move a waypoint which is relative to the ship's position:

Action N means to move the waypoint north by the given value.
Action S means to move the waypoint south by the given value.
Action E means to move the waypoint east by the given value.
Action W means to move the waypoint west by the given value.
Action L means to rotate the waypoint around the ship left (counter-clockwise) the given number of degrees.
Action R means to rotate the waypoint around the ship right (clockwise) the given number of degrees.
Action F means to move forward to the waypoint a number of times equal to the given value.
The waypoint starts 10 units east and 1 unit north relative to the ship. The waypoint is relative to the ship; that is, if the ship moves,
the waypoint moves with it.

For example, using the same instructions as above:

F10 moves the ship to the waypoint 10 times (a total of 100 units east and 10 units north), leaving the ship at east 100, north 10.
The waypoint stays 10 units east and 1 unit north of the ship.
N3 moves the waypoint 3 units north to 10 units east and 4 units north of the ship. The ship remains at east 100, north 10.
F7 moves the ship to the waypoint 7 times (a total of 70 units east and 28 units north), leaving the ship at east 170, north 38.
The waypoint stays 10 units east and 4 units north of the ship.
R90 rotates the waypoint around the ship clockwise 90 degrees, moving it to 4 units east and 10 units south of the ship. The ship remains at east 170, north 38.
F11 moves the ship to the waypoint 11 times (a total of 44 units east and 110 units south), leaving the ship at east 214, south 72.
The waypoint stays 4 units east and 10 units south of the ship.
After these operations, the ship's Manhattan distance from its starting position is 214 + 72 = 286.

Figure out where the navigation instructions actually lead. What is the Manhattan distance between that location and the ship's starting position?

Your puzzle answer was 29839.

Both parts of this puzzle are complete! They provide two gold stars: **
"""

from advent.tools import *


class Instruction(t.NamedTuple):
    action: str
    value: int


@dc.dataclass
class Ship:
    coords = (0, 0)
    facing = "E"
    dirs = {
        "N": lambda c, v: (c[0], c[1] + v),
        "E": lambda c, v: (c[0] + v, c[1]),
        "S": lambda c, v: (c[0], c[1] - v),
        "W": lambda c, v: (c[0] - v, c[1]),
    }

    def apply(self, ins: Instruction):
        self.facing = self._next_facing(ins)
        self._move(*self._next_move(ins))

    def manhattan_distance(self, coords: t.Tuple[int, int] = (0, 0)) -> int:
        return abs(self.coords[0] - coords[0]) + abs(self.coords[1] - coords[1])

    def _move(self, d: str, v: int):
        self.coords = self.dirs[d](self.coords, v)

    def _next_move(self, ins: Instruction) -> t.Tuple[str, int]:
        if ins.action in {"L", "R"}:
            return self.facing, 0
        if ins.action == "F":
            return self.facing, ins.value
        return ins.action, ins.value

    def _next_facing(self, ins: Instruction) -> str:
        if ins.action in {"L", "R"}:
            dirs = list(self.dirs.keys())
            rot = ins.value // 90
            rot = -rot if ins.action == "L" else rot
            cur = dirs.index(self.facing)
            return dirs[(cur + rot) % len(dirs)]

        return self.facing


class WaypointShip(Ship):
    waypoint_offset = (10, 1)

    def apply(self, ins: Instruction):
        if ins.action in self.dirs:
            self._move_waypoint(ins.action, ins.value)
        elif ins.action == "F":
            self._move_ship(ins.value)
        else:
            self._rotate_waypoint(ins.action, ins.value)

    def _move_ship(self, v: int):
        y, x = self._waypoint_cardinal
        off = self.waypoint_offset
        self._move(y, v * abs(off[1]))
        self._move(x, v * abs(off[0]))

    def _move_waypoint(self, d: str, v: int):
        self.waypoint_offset = self.dirs[d](self.waypoint_offset, v)

    def _rotate_waypoint(self, d: str, v: int):
        rot = math.radians(-v if d == "R" else v)
        wp, c = self._waypoint, self.coords
        sr, cr, ax, ay = math.sin(rot), math.cos(rot), wp[0] - c[0], wp[1] - c[1]
        nx, ny = c[0] + cr * ax - sr * ay, c[1] + sr * ax + cr * ay
        self.waypoint_offset = (int(nx) - c[0], int(ny) - c[1])

    @property
    def _waypoint_cardinal(self) -> t.Tuple[str, str]:
        ns = "N" if self.waypoint_offset[1] > 0 else "S"
        ew = "E" if self.waypoint_offset[0] > 0 else "W"
        return ns, ew

    @property
    def _waypoint(self) -> t.Tuple[int, int]:
        c, w = self.coords, self.waypoint_offset
        return (c[0] + w[0], c[1] + w[1])


def _follow_instructions(ship: Ship, instructions: t.List[Instruction]):
    for ins in instructions:
        ship.apply(ins)

    return ship.manhattan_distance()


def _pt1(lines):
    return _follow_instructions(Ship(), lines)


def _pt2(lines):
    return _follow_instructions(WaypointShip(), lines)


TEST = """F10
N3
F7
R90
F11"""


def _transform(line):
    action, value = re.match(r"^([A-Z])(\d+)", line).groups()
    return Instruction(action, int(value))


def main():
    return afs.input_lines(
        parts=[_pt1, _pt2],
        tests=[TEST],
        transform_line=_transform,
    )
