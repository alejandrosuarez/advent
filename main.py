#!/usr/bin/env python3

from sys import argv


def main():
    y, d = f"year_{argv[1]}", f"day_{argv[2]}"
    mod = __import__(f"advent.{y}.{d}")
    day = getattr(getattr(mod, y), d)
    return day.main()


if __name__ == "__main__":
    print(main())