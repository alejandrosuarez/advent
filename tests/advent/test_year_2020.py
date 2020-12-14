from advent.year_2020 import day_12, day_13


def test_day_12():
    lines = """F10
N3
F7
R90
F11""".splitlines()

    pt1 = day_12.follow_instructions(day_12.Ship(), lines)
    assert pt1 == 25

    pt2 = day_12.follow_instructions(day_12.WaypointShip(), lines)
    assert pt2 == 286


def test_day_13():
    lines = "939\n7,13,x,x,59,x,31,19".splitlines()
    pt1 = day_13.pt1(lines)

    assert pt1 == 295
