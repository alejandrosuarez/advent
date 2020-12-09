from dataclasses import dataclass, field
from typing import List, Callable, Dict


@dataclass
class Instruction:
    name: str
    arity: int
    func: Callable


@dataclass
class VM:
    instruction_table: Dict[str, Instruction]
    cursor: int = 0
    local: Dict = field(default_factory=dict)
    instructions: List = field(default_factory=list)

    def run(self):
        while self.cursor < len(self.instructions):
            name, args = self.instructions[self.cursor]
            ins = self.instruction_table[name]
            ins.func(self, args)