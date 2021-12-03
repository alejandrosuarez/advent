from inspect import stack
from os import path, system
from re import sub, match

TMPL = '''"""
"""

from advent.tools import *


def _pt1(lines):
    pass


def _pt2(lines):
    pass


TEST = """
"""
ANSWERS = None


def main():
    return afs.input_lines(tests=[TEST], parts=[_pt1], run_input=False)

'''


def with_caller(func):
    def wrapper(*args, **kwargs):
        caller = stack()[1].filename
        return func(caller, *args, **kwargs)

    return wrapper


def load_input(caller=None):
    caller = stack()[1].filename if not caller else caller
    input_path = sub(r"\.py", ".txt", caller)

    return open(input_path, "r")


def read_input(caller=None):
    caller = stack()[1].filename if not caller else caller
    return load_input(caller).read()


@with_caller
def input_lines(
    caller,
    tests=[],
    parts=[],
    transform_lines=lambda g: g,
    transform_line=lambda l: l,
    run_input=True,
):
    inputs = tests + ([read_input(caller)] if run_input else [])
    results = []

    for part in parts:
        for inp in inputs:
            args = list(map(transform_line, transform_lines(inp.splitlines())))
            results.append(part(args))

    return results


@with_caller
def input_groups(
    caller,
    tests=[],
    parts=[],
    transform_groups=lambda g: g,
    transform_group=lambda g: g,
    sep="\n\n",
):
    inputs = tests + [read_input(caller)]
    results = []

    for part in parts:
        for inp in inputs:
            args = list(
                map(
                    transform_group,
                    transform_groups(inp.split(sep)),
                )
            )

            results.append(part(args))

    return results


def run(year, day):
    y, d = f"year_{year}", f"day_{day}"
    mod = __import__(f"advent.{y}.{d}")
    day = getattr(getattr(mod, y), d)
    return day.main()


def run_file(path):
    return run(*match(r"^.*/advent/year_(\d+)/day_(\d+).py", path).groups())


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
