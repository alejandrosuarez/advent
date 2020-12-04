from sys import argv
from advent import DAYS


def main():
    return DAYS[int(argv[1])].main()


if __name__ == "__main__":
    print(main())