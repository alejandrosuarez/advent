"""
"""

from advent.tools import *

import string

ALPHABET = list(string.ascii_lowercase)
STRAIGHTS = ["".join(s) for s in zip(ALPHABET, ALPHABET[1:], ALPHABET[2:])]


def _valid_password(password):
    no_bad_letters = not re.search(r"[iol]", password)
    has_straight = any(s in password for s in STRAIGHTS)
    pairs = {a for a, b in zip(password, password[1:]) if a == b}
    has_pairs = len(pairs) > 1
    return has_straight and no_bad_letters and has_pairs


def _incrementing_passwords(password):
    pass


def _pt1(lines):
    return next(p for p in _incrementing_passwords(lines[0]) if _valid_password(p))


def _pt2(lines):
    pass


ANSWERS = None
TEST1 = "hijklmmn"
TEST2 = "abbceffg"
TEST3 = "abbcegjk"
TEST4 = "abcdffaa"
TEST5 = "ghjaabcc"


def main():
    assert not _valid_password(TEST1)
    assert not _valid_password(TEST2)
    assert not _valid_password(TEST3)
    assert _valid_password(TEST4)
    assert _valid_password(TEST5)

    return afs.input_lines(tests=[TEST4, TEST5], parts=[_pt1], run_input=True)
