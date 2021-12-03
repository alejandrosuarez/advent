#!/usr/bin/env python3

from sys import argv

from advent.fs import generate, run, run_file


def main():
    return {"run": run, "generate": generate, "run-file": run_file}[argv[1]](*argv[2:])


if __name__ == "__main__":
    print(main())
