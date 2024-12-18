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


class Opcode(Enum):
    ADV = 0
    BXL = 1
    BST = 2
    JNZ = 3
    BXC = 4
    OUT = 5
    BDV = 6
    CDV = 7


def combo(registers, operand):
    match operand:
        case 0 | 1 | 2 | 3:
            return operand, str(operand)
        case 4:
            return registers.a, "a"
        case 5:
            return registers.b, "b"
        case 6:
            return registers.c, "c"
        case _:
            raise ValueError(f"Invalid combo operand {operand}")


def _dv(registers, operand):
    co, ser = combo(registers, operand)
    return registers.a // (2 ** co), ser


def adv(registers, operand):
    res, ser = _dv(registers, operand)
    return Registers(res, registers.b, registers.c), f"a = a // 2 ** {ser}"


def bxl(registers, operand):
    return Registers(registers.a, registers.b ^ operand, registers.c), f"b = b ^ {operand}"


def bst(registers, operand):
    co, ser = combo(registers, operand)
    return Registers(registers.a, co % 8, registers.c), f"b = {ser} % 8"


def jnz(registers, operand, ip):
    return ip + 2 if registers.a == 0 else operand, "JNZ"


def bxc(registers, operand):
    return Registers(registers.a, registers.b ^ registers.c, registers.c), "b = b ^ c"


def out(registers, operand):
    co, ser = combo(registers, operand)
    return co % 8, f"stdout.append({ser} % 8)"


def bdv(registers, operand):
    res, ser = _dv(registers, operand)
    return Registers(registers.a, res, registers.c), f"b = a // 2 ** {ser}"


def cdv(registers, operand):
    res, ser = _dv(registers, operand)
    return Registers(registers.a, registers.b, res), f"c = a // 2 ** {ser}"


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
            registers, _ = op(registers, operand)
            ip += 2
        elif opcode == Opcode.JNZ:
            ip, _ = jnz(registers, operand, ip)
        elif opcode == Opcode.OUT:
            o, _ = out(registers, operand)
            stdout.append(o)
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


def manual_for_a(a):
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


def transpile(registers, program):
    stdout = []
    ip = 0
    pstr = []
    while ip < len(program):
        opcode = Opcode(program[ip])
        operand = program[ip + 1]
        if op := operations.get(opcode):
            registers, loc = op(registers, operand)
            ip += 2
        elif opcode == Opcode.JNZ:
            ip, loc = jnz(registers, operand, ip)
            return pstr
        elif opcode == Opcode.OUT:
            o, loc = out(registers, operand)
            stdout.append(o)
            ip += 2
        pstr.append(loc)
    return pstr


def simplified_for_a(pstr):
    """
    Given a simplified program, return a function that computes it for any value of A.
    """
    function = """
def p(a):
    b = c = 0
    stdout = []
    while a:
"""
    for line in pstr:
        function += f"        {line}\n"

    function += "    return stdout\n"
    print(function)
    exec(function, globals())
    return globals()["p"]


def part2():
    """Find a value for A such that program p is a Quine, i.e. p(a) == p()"""
    registers, program = parse_data(read_input())
    python_program = simplified_for_a(transpile(registers, program))

    candidates = {0}
    # Starting from the last instruction (since it's the easiest),
    # Work backward with greater and greater A values until we have the coplete program.
    for instruction in reversed(program):
        new_candidates = set()
        for a in candidates:
            shifted = a * 8
            for candidate in range(shifted, shifted+8):
                stdout = python_program(candidate)
                if stdout and stdout[0] == instruction:
                    new_candidates.add(candidate)
        candidates = new_candidates
    return min(candidates)


if __name__ == "__main__":
    print(part2())
