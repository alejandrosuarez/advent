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
    other_inputs=[],
    parts=[],
    transform_lines=lambda g: g,
    transform_line=lambda l: l,
):
    inputs = other_inputs + [read_input(caller)]
    results = []

    for part in parts:
        for inp in inputs:
            args = list(map(transform_line, transform_lines(inp.splitlines())))
            results.append(part(args))

    return results


@with_caller
def input_groups(
    caller,
    other_inputs=[],
    parts=[],
    transform_groups=lambda g: g,
    transform_group=lambda g: g,
    sep="\n\n",
):
    inputs = other_inputs + [read_input(caller)]
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
