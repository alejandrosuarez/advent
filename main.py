#!/usr/bin/env python3

from sys import argv

from advent.fs import generate, run


def main():
    return {"run": run, "generate": generate}[argv[1]](*argv[2:])


if __name__ == "__main__":
    print(main())
