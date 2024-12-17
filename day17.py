import sys
from typing import NamedTuple


def read_input():
    with open(sys.argv[1]) as f:
        return f.read().strip()


class Registers(NamedTuple):
    a: int
    b: int
    c: int

    def write(self, register, value):
        match register:
            case "a":
                return Registers(value, self.b, self.c)
            case "b":
                return Registers(self.a, value, self.c)
            case "c":
                return Registers(self.a, self.b, value)
            case _:
                raise ValueError(f"Invalid register {register}")


Instruction = int
Program = list[Instruction]


class Computer:
    registers: Registers
    program: Program
    instruction_pointer: int
    stdout: list[int]
    __slots__ = ["registers", "program", "instruction_pointer", "stdout"]

    def __init__(self, registers, program):
        self.registers = registers
        self.program = program
        self.instruction_pointer = 0
        self.stdout = []

    def dump_stdout(self):
        return ",".join(map(str, self.stdout))

    @property
    def opcode(self):
        return self.program[self.instruction_pointer]

    @property
    def operand(self):
        return self.program[self.instruction_pointer + 1]

    @property
    def combo(self):
        match self.operand:
            case 0 | 1 | 2 | 3:
                return self.operand
            case 4:
                return self.registers.a
            case 5:
                return self.registers.b
            case 6:
                return self.registers.c
            case _:
                raise ValueError(f"Invalid combo operand {self.operand}")

    def advance(self):
        self.instruction_pointer += 2
        return self

    def _adv(self):
        assert self.opcode == 0
        numerator = self.registers.a
        denominator = 2**self.combo
        result = numerator // denominator
        self.registers = self.registers.write("a", result)
        return self.advance()

    def _bxl(self):
        assert self.opcode == 1
        bitwise_xor = self.registers.b ^ self.operand
        self.registers = self.registers.write("b", bitwise_xor)
        return self.advance()

    def _bst(self):
        assert self.opcode == 2
        result = self.combo % 8
        self.registers = self.registers.write("b", result)
        return self.advance()

    def _jnz(self):
        assert self.opcode == 3
        if self.registers.a == 0:
            return self.advance()
        self.instruction_pointer = self.operand
        return self

    def _bxc(self):
        assert self.opcode == 4
        bitwise_xor = self.registers.b ^ self.registers.c
        self.registers = self.registers.write("b", bitwise_xor)
        return self.advance()

    def _out(self):
        assert self.opcode == 5
        self.stdout.append(self.combo % 8)
        return self.advance()

    def _bdv(self):
        assert self.opcode == 6
        numerator = self.registers.a
        denominator = 2**self.combo
        result = numerator // denominator
        self.registers = self.registers.write("b", result)
        return self.advance()

    def _cdv(self):
        assert self.opcode == 7
        numerator = self.registers.a
        denominator = 2**self.combo
        result = numerator // denominator
        self.registers = self.registers.write("c", result)
        return self.advance()

    def run(self):
        match self.opcode:
            case 0:
                return self._adv()
            case 1:
                return self._bxl()
            case 2:
                return self._bst()
            case 3:
                return self._jnz()
            case 4:
                return self._bxc()
            case 5:
                return self._out()
            case 6:
                return self._bdv()
            case 7:
                return self._cdv()
            case _:
                raise ValueError(f"Invalid opcode {self.opcode}")

    def run_until_next_output(self):
        before = len(self.stdout)
        while not self.halted:
            self = self.run()
            if len(self.stdout) > before:
                return self
        return self

    @property
    def halted(self):
        return self.instruction_pointer >= len(self.program)

    def __str__(self):
        return (
            f"Computer(registers={self.registers}, "
            f"program={self.program}, "
            f"instruction_pointer={self.instruction_pointer}, "
            f"stdout={self.dump_stdout()})"
        )


def parse_data(data):
    lines = data.splitlines()

    def extract_register_value(line):
        return int(line.split()[-1])

    registers = Registers(*map(extract_register_value, lines[:3]))
    instructions = [int(x) for x in lines[-1].split()[-1].split(",")]
    return registers, instructions


def part1():
    registers, program = parse_data(read_input())
    computer = Computer(registers, program)
    while computer.instruction_pointer < len(computer.program):
        computer = computer.run()
    return computer.dump_stdout()


def matches_prefix(prefix, full):
    return all(a == b for a, b in zip(prefix, full))


def part2():
    _, program = parse_data(read_input())
    print(program)
    # We are searching for a quine of program based on Register A.
    # We'll do this with a computation tree - only run programs that keep generating the right values.
    # So, advancing through candidate values for A, we'll run each computer until it generates a bad value.
    # If it never generates a bad value, we've done it!
    a = 0
    while True:
        registers = Registers(a, 0, 0)
        computer = Computer(registers, program)
        while computer.instruction_pointer < len(computer.program):
            computer = computer.run_until_next_output()
            if not matches_prefix(computer.stdout, program):
                break
            else:
                print("A:", a, "stdout:", computer.dump_stdout())
                if len(computer.stdout) == len(program):
                    print(computer.dump_stdout())
                    return a
        a += 1


if __name__ == "__main__":
    print(part1())
