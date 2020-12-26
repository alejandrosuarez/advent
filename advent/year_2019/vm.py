from advent.tools import *


@dc.dataclass
class Instruction:
    opcode: int
    name: str
    arity: int
    func: t.Callable


@dc.dataclass
class VM:
    instructions: t.List[Instruction]
    cursor: int = 0
    local: t.Dict = dc.field(default_factory=dict)
    code: t.List = dc.field(default_factory=list)

    def __post_init__(self):
        self.instruction_table = {i.opcode: i for i in self.instructions}

    def run(self):
        while self.cursor < len(self.code):
            self._cycle(self.cursor)

    def read(self, addr: int, mode: int) -> int:
        return addr if mode == 1 else self.code[addr]

    def _get_opcode(self, val: int) -> int:
        return val % 100

    def _get_modes(self, val: int, ins: Instruction) -> t.List[int]:
        n, i, modes = val // 100, 0, [0] * ins.arity

        while n > 0:
            modes[i] = n % 10
            n //= 10
            i += 1

        return modes

    def _cycle(self, cur: int):
        instruction = self.code[cur]
        opcode = self._get_opcode(instruction)
        ins = self.instruction_table[opcode]
        modes = self._get_modes(instruction, ins)
        args = self.code[cur + 1 : cur + ins.arity + 1]
        ins.func(self, args, modes)


class AddInstruction(Instruction):
    opcode = 1
    name = "add"
    arity = 3

    @staticmethod
    def func(vm: VM, args: t.List[int], modes: t.List[int]):
        x, y, z = args
        xm, ym, _ = modes
        vm.code[z] = vm.read(x, xm) + vm.read(y, ym)
        vm.cursor += 4


class MultiplyInstruction(Instruction):
    opcode = 2
    name = "multiply"
    arity = 3

    @staticmethod
    def func(vm: VM, args: t.List[int], modes: t.List[int]):
        x, y, z = args
        xm, ym, _ = modes
        vm.code[z] = vm.read(x, xm) * vm.read(y, ym)
        vm.cursor += 4


class SaveInstruction(Instruction):
    opcode = 3
    name = "save"
    arity = 1

    @staticmethod
    def func(vm: VM, args: t.List[int], _modes: t.List[int]):
        cur = vm.local.setdefault("input_cursor", 0)
        vm.code[args[0]] = vm.local["input"][cur]
        vm.cursor += 2
        vm.local["input_cursor"] += 1


class OutputInstruction(Instruction):
    opcode = 4
    name = "output"
    arity = 1

    @staticmethod
    def func(vm: VM, args: t.List[int], _modes: t.List[int]):
        vm.local.setdefault("output", []).append(vm.code[args[0]])
        vm.cursor += 2


class ExitInstruction(Instruction):
    opcode = 99
    name = "exit"
    arity = 0

    @staticmethod
    def func(vm: VM, _args: t.List[int], _modes: t.List[int]):
        vm.cursor = len(vm.code)


class JumpIfTrueInstruction(Instruction):
    opcode = 5
    name = "jump-if-true"
    arity = 2

    @staticmethod
    def func(vm: VM, args: t.List[int], modes: t.List[int]):
        pointer = vm.read(args[0], modes[0])

        if pointer != 0:
            vm.cursor = vm.read(args[1], modes[1])
        else:
            vm.cursor += 3


class JumpIfFalseInstruction(Instruction):
    opcode = 6
    name = "jump-if-false"
    arity = 2

    @staticmethod
    def func(vm: VM, args: t.List[int], modes: t.List[int]):
        pointer = vm.read(args[0], modes[0])

        if pointer == 0:
            vm.cursor = vm.read(args[1], modes[1])
        else:
            vm.cursor += 3


class LessThanInstruction(Instruction):
    opcode = 7
    name = "less-than"
    arity = 3

    @staticmethod
    def func(vm: VM, args: t.List[int], modes: t.List[int]):
        x = vm.read(args[0], modes[0])
        y = vm.read(args[1], modes[1])
        z = args[2]
        vm.code[z] = int(x < y)
        vm.cursor += 4


class GreaterThanInstruction(Instruction):
    opcode = 8
    name = "greater-than"
    arity = 3

    @staticmethod
    def func(vm: VM, args: t.List[int], modes: t.List[int]):
        x = vm.read(args[0], modes[0])
        y = vm.read(args[1], modes[1])
        z = args[2]
        vm.code[z] = int(x == y)
        vm.cursor += 4