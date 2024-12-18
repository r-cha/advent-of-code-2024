import sys

from sympy import Eq, Mod, S, init_printing, solve, symbols


def read_input():
    with open(sys.argv[1]) as f:
        return f.read().strip()


class Registers:
    __slots__ = ["a", "b", "c"]

    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def write(self, register, value):
        if register == "a":
            return Registers(value, self.b, self.c)
        elif register == "b":
            return Registers(self.a, value, self.c)
        elif register == "c":
            return Registers(self.a, self.b, value)
        else:
            raise ValueError(f"Invalid register {register}")

    def __repr__(self):
        return f"Registers(a={self.a}, b={self.b}, c={self.c})"


def combo(registers, operand):
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


def _dv(registers, operand):
    return registers.a // (2 ** combo(registers, operand))


def adv(registers, operand):
    return Registers(_dv(registers, operand), registers.b, registers.c)


def bxl(registers, operand):
    return Registers(registers.a, registers.b ^ S(operand), registers.c)


def bst(registers, operand):
    return Registers(
        registers.a, Mod(combo(registers, operand), 8, evaluate=False), registers.c
    )


def jnz(registers, operand, ip):
    return ip + 2 if registers.a == 0 else operand


def bxc(registers, operand):
    return Registers(registers.a, registers.b ^ registers.c, registers.c)


def out(registers, operand):
    return Mod(combo(registers, operand), 8, evaluate=False)


def bdv(registers, operand):
    return Registers(registers.a, _dv(registers, operand), registers.c)


def cdv(registers, operand):
    return Registers(registers.a, registers.b, _dv(registers, operand))


operations = {
    0: adv,
    1: bxl,
    2: bst,
    4: bxc,
    6: bdv,
    7: cdv,
}


def interpret(r, program):
    registers = r
    stdout = []
    ip = 0
    while ip < len(program):
        opcode = program[ip]
        operand = program[ip + 1]
        # print(ip, opcode, operand, registers, stdout)
        if op := operations.get(opcode):
            registers = op(registers, operand)
            ip += 2
        elif opcode == 3:
            ip = jnz(registers, operand, ip)
        elif opcode == 5:
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


def symbolic_interpret(r, program):
    registers = r
    stdout = []
    ip = 0
    while ip < len(program):
        opcode = program[ip]
        operand = program[ip + 1]
        if op := operations.get(opcode):
            registers = op(registers, operand)
            ip += 2
        elif opcode == 3:
            ip = jnz(registers, operand, ip)
        elif opcode == 5:
            stdout.append(out(registers, operand))
            ip += 2
    return stdout


def part2():
    _, program = parse_data(read_input())
    # Define symbolic variables
    A, B, C = symbols("A B C", integer=True, nonnegative=True)
    initial_registers = Registers(A, B, C)
    # Perform symbolic execution
    symbolic_stdout = symbolic_interpret(initial_registers, program)
    init_printing(use_unicode=True)
    print(symbolic_stdout)
    # Create equations where each stdout element equals the corresponding program instruction
    equations = [Eq(expr, program[i]) for i, expr in enumerate(symbolic_stdout)]
    # Solve for A
    solution = solve(equations, A)
    return solution


if __name__ == "__main__":
    print(part1())
    print(part2())
