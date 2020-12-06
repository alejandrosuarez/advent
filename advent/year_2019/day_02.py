"""
0 = opcode
    1 = add 2 nums, store in 3rd pos
    2
    99 = halt
    unknown = bad
"""

from advent.util import load_input


def _program(nums, noun, verb):
    nums[1], nums[2] = noun, verb

    def run(i):
        if nums[i] == 99:
            return

        a, b, p = nums[i + 1 : i + 4]

        if nums[i] == 1:
            nums[p] = nums[a] + nums[b]
        else:
            nums[p] = nums[a] * nums[b]

        run(i + 4)

    run(0)
    return nums[0]


def main():
    a = [int(n) for n in load_input().read().strip().split(",")]
    k = 19690720

    for n in range(100):
        for v in range(100):
            result = _program(a[:], n, v)

            if result == k:
                return 100 * n + v