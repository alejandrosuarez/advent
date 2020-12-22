from os import path
from inspect import stack
from re import sub


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