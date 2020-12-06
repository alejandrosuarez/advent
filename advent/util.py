from os import path
from inspect import stack
from re import sub


def load_input():
    dir_path = path.dirname(path.realpath(__file__))
    caller_fname = stack()[1].filename
    day = path.basename(caller_fname).split(".")[0]
    input_path = sub(r"\.py", ".txt", caller_fname)

    return open(input_path, "r")
