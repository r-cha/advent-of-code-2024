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
            print(operand)
            return operand
        case 4:
            print("a")
            return registers.a
        case 5:
            print("b")
            return registers.b
        case 6:
            print("c")
            return registers.c
        case _:
            raise ValueError(f"Invalid combo operand {operand}")


def _dv(registers: Registers, operand: int) -> int:
    return registers.a // (2 ** combo(registers, operand))


def adv(registers, operand):
    print("a = a/2^", end="")
    return Registers(_dv(registers, operand), registers.b, registers.c)


def bxl(registers, operand):
    print(f"b = b ^ {operand}")
    return Registers(registers.a, registers.b ^ operand, registers.c)


def bst(registers, operand):
    print(f"b = ", end="")
    co = combo(registers, operand)
    print( "% 8")
    return Registers(registers.a, combo(registers, operand) % 8, registers.c)


def jnz(registers, operand, ip):
    print("JNZ")
    return ip + 2 if registers.a == 0 else operand


def bxc(registers, operand):
    print("b = b ^ c")
    return Registers(registers.a, registers.b ^ registers.c, registers.c)


def out(registers, operand):
    co = combo(registers, operand)
    print(f"OUT {co} % 8")
    return co % 8


def bdv(registers, operand):
    print("b = a/2^", end="")
    return Registers(registers.a, _dv(registers, operand), registers.c)


def cdv(registers, operand):
    print("c = a/2^", end="")
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


def simplified_test_for_a(a):
    stdout = []
    while a:
        a = a >> 3 # a // 8
        res.append(a % 8)
    return res


def simplified_for_a(a):
    """
    For my program,
    > 2,4,1,5,7,5,1,6,4,1,5,5,0,3,3,0
    I can simplify it to these basic commands.
    """
    b = c = 0
    stdout = []

    while a:
        b = a % 8
        b = b ^ 5
        c = a // 2**b
        b = b ^ 6
        b = b ^ c
        stdout.append(b % 8)
        a = a >> 8

    return stdout


def part2():
    """Find a value for A such that program p is a Quine, i.e. p(a) == p()"""
    _, p = parse_data(read_input())
    candidates = {0}
    # Starting from the last instruction (since it's the easiest),
    # Work backward with greater and greater A values until we have the coplete program.
    for instruction in reversed(p):
        new_candidates = set()
        for a in candidates:
            shifted = a * 8
            for candidate in range(shifted, shifted+8):
                stdout = simplified_for_a(candidate)
                if stdout and stdout[0] == instruction:
                    new_candidates.add(candidate)
        candidates = new_candidates
    return min(candidates)


if __name__ == "__main__":
    print(part2())
