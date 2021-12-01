"""
"""

from advent.tools import *

from .vm import (
    VM,
    AddInstruction,
    ExitInstruction,
    GreaterThanInstruction,
    JumpIfFalseInstruction,
    JumpIfTrueInstruction,
    LessThanInstruction,
    MultiplyInstruction,
    OutputInstruction,
    SaveInstruction,
)


def _run(code, input_signal, phase_setting):
    vm = VM(
        instructions=[
            AddInstruction,
            ExitInstruction,
            MultiplyInstruction,
            SaveInstruction,
            OutputInstruction,
            JumpIfTrueInstruction,
            JumpIfFalseInstruction,
            LessThanInstruction,
            GreaterThanInstruction,
        ],
        code=code,
        local={"input": [phase_setting, input_signal]},
    )

    vm.run()

    return vm.local["output"][-1]


def _pt1(code):
    ans = float("-inf")

    for seq in it.permutations(range(5)):
        output = ft.reduce(lambda o, s: _run(code, o, s), seq, 0)
        ans = max(ans, output)

    return ans


def _pt2(code):
    pass


TEST1 = "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"
TEST2 = "3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0"
TEST3 = "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0"
TEST4 = "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5"
TEST5 = "3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10"


def main():
    return afs.input_lines(
        tests=[TEST4, TEST5],
        parts=[_pt2],
        run_input=False,
        transform_lines=lambda l: l[0].split(","),
        transform_line=int,
    )
