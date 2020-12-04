from os import path
from inspect import stack


def load_input():
    dir_path = path.dirname(path.realpath(__file__))
    caller_fname = stack()[1].filename
    day = path.basename(caller_fname).split(".")[0]
    input_path = f"{dir_path}/days/{day}_input.txt"

    return open(input_path, "r")
