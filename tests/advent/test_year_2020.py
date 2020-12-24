from pytest import mark
from advent.year_2020 import *


def test_day_01():
    assert day_01.main() == [514579, 197451, 241861950, 138233720]


def test_day_02():
    assert day_02.main() == [[2, 1], [414, 413]]


def test_day_03():
    assert day_03.main() == [7, 145, 336, 3424528800]


@mark.skip
def test_day_04():
    assert day_04.main() == ""


def test_day_05():
    assert day_05.main() == [(944, 554)]


def test_day_06():
    assert day_06.main() == [11, 6259, 6, 3178]


def test_day_07():
    assert day_07.main() == [4, 355, 32, 5312]


def test_day_08():
    assert day_08.main() == [5, 1709, 8, 1976]


def test_day_09():
    assert day_09.main() == [133015568, 16107959]


def test_day_10():
    assert day_10.main() == [35, 1984, 8, 3543369523456]


@mark.skip
def test_day_11():
    assert day_11.main() == [37, 2296, 26, 2089]


def test_day_12():
    assert day_12.main() == [25, 2847, 286, 29839]


def test_day_13():
    assert day_13.main() == [296, 535296695251210]


def test_day_14():
    assert day_14.main() == [
        165,
        16003257187056,
        51,
        16003257187056,
        208,
        3219837697833,
    ]


@mark.skip
def test_day_15():
    assert day_15.main() == [436, 1696, 175594, 37385]


def test_day_16():
    assert day_16.main() == [71, 0, 27802, 1, 1, 279139880759]


@mark.skip
def test_day_17():
    assert day_17.main() == [112, 265, 848, 1936]


def test_day_18():
    assert day_18.main() == [26457, 26457, 701339185745, 694173, 694173, 4208490449905]


@mark.skip
def test_day_19():
    assert day_19.main() == [2, 3, 118, 2, 12, 246]


def test_day_20():
    assert day_20.main() == [20899048083289, 15003787688423, 273, 1705]


def test_day_21():
    assert day_21.main() == [
        5,
        2436,
        "mxmxvkd,sqjhc,fvjkl",
        "dhfng,pgblcd,xhkdc,ghlzj,dstct,nqbnmzx,ntggc,znrzgs",
    ]


@mark.skip
def test_day_22():
    assert day_22.main() == [306, 32783, 291, 33455]


@mark.skip
def test_day_23():
    assert day_23.main() == [
        ("92658374", "67384529"),
        ("42573968", "28793654"),
        149245887792,
        359206768694,
    ]


def test_day_24():
    assert day_24.main() == [2, 10, 330, 0, 2208, 3711]