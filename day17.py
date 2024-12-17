import sys
from enum import Enum
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


class Opcode(Enum):
    ADV = 0
    BXL = 1
    BST = 2
    JNZ = 3
    BXC = 4
    OUT = 5
    BDV = 6
    CDV = 7


def combo(registers: Registers, operand: int) -> int:
    match operand:
        case 0 | 1 | 2 | 3:
            return operand
        case 4:
            return registers.a
        case 5:
            return registers.b
        case 6:
            return registers.c
        case _:
            raise ValueError(f"Invalid combo operand {operand}")


def _dv(registers: Registers, operand: int) -> int:
    return registers.a // (2 ** combo(registers, operand))


def adv(registers, operand):
    return Registers(_dv(registers, operand), registers.b, registers.c)


def bxl(registers, operand):
    return Registers(registers.a, registers.b ^ operand, registers.c)


def bst(registers, operand):
    return Registers(registers.a, combo(registers, operand) % 8, registers.c)


def jnz(registers, operand, ip):
    return ip + 2 if registers.a == 0 else operand


def bxc(registers, operand):
    return Registers(registers.a, registers.b ^ registers.c, registers.c)


def out(registers, operand):
    return combo(registers, operand) % 8


def bdv(registers, operand):
    return Registers(registers.a, _dv(registers, operand), registers.c)


def cdv(registers, operand):
    return Registers(registers.a, registers.b, _dv(registers, operand))


operations = {
    Opcode.ADV: adv,
    Opcode.BXL: bxl,
    Opcode.BST: bst,
    Opcode.BXC: bxc,
    Opcode.BDV: bdv,
    Opcode.CDV: cdv,
}


def interpret(r, program):
    registers = r
    stdout = []
    ip = 0
    while ip < len(program):
        opcode = Opcode(program[ip])
        operand = program[ip + 1]
        # print(ip, opcode, operand, registers, stdout)
        if op := operations.get(opcode):
            registers = op(registers, operand)
            ip += 2
        elif opcode == Opcode.JNZ:
            ip = jnz(registers, operand, ip)
        elif opcode == Opcode.OUT:
            stdout.append(out(registers, operand))
            ip += 2
    return stdout


def dump(stdout):
    return ",".join(map(str, stdout))


def parse_data(data):
    lines = data.splitlines()

    def extract_register_value(line):
        return int(line.split()[-1])

    registers = Registers(*map(extract_register_value, lines[:3]))
    instructions = [int(x) for x in lines[-1].split()[-1].split(",")]
    return registers, instructions


def part1():
    registers, program = parse_data(read_input())
    stdout = interpret(registers, program)
    return dump(stdout)


if __name__ == "__main__":
    print(part1())
