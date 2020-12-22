from os import path, system
from inspect import stack
from re import sub

TMPL = '''"""
"""

from advent.tools import *

TEST = """
"""


def main():
    pass
'''


def load_input(caller=None):
    caller = stack()[1].filename if not caller else caller
    input_path = sub(r"\.py", ".txt", caller)

    return open(input_path, "r")


def read_input(caller=None):
    caller = stack()[1].filename if not caller else caller
    return load_input(caller).read()


def input_lines():
    caller = stack()[1].filename
    return read_input(caller).splitlines()


def run(year, day):
    y, d = f"year_{year}", f"day_{day}"
    mod = __import__(f"advent.{y}.{d}")
    day = getattr(getattr(mod, y), d)
    return day.main()


def generate(year, day):
    p = path.dirname(path.realpath(__file__))
    fpath = f"{p}/year_{year}/day_{day}"
    pyfile = f"{fpath}.py"
    txtfile = f"{fpath}.txt"

    if not path.exists(txtfile):
        open(f"{fpath}.txt", "w+")

    if not path.exists(pyfile):
        with open(pyfile, "a+") as f:
            f.write(TMPL)

    system(f"code {pyfile}")
    return ""
