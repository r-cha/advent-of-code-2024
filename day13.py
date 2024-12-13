import re
import sys
from itertools import product
from typing import NamedTuple


def read_input():
    if len(sys.argv) == 2:
        with open(sys.argv[1], "r") as f:
            return f.read().strip()
    return sys.stdin.read().strip()


A_COST = 3
B_COST = 1


class Vector(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, value: int) -> "Vector":
        return Vector(self.x * value, self.y * value)


class Machine(NamedTuple):
    a: Vector
    b: Vector
    prize: Vector

    def offset_prize(self, offset: int) -> "Machine":
        return Machine(self.a, self.b, self.prize + Vector(offset, offset))


def parse_data(data) -> list[Machine]:
    machines = []
    lines = data.split("\n\n")
    for desc in lines:
        astr, bstr, prize = desc.splitlines()
        ax, ay = map(int, re.findall(r"X\+(\d+), Y\+(\d+)", astr)[0])
        bx, by = map(int, re.findall(r"X\+(\d+), Y\+(\d+)", bstr)[0])
        px, py = map(int, re.findall(r"X=(\d+), Y=(\d+)", prize)[0])
        machines.append(Machine(Vector(ax, ay), Vector(bx, by), Vector(px, py)))
    return machines


def determine_cost(machine: Machine) -> int:
    min_cost = float("inf")

    for a_presses, b_presses in product(range(101), range(101)):
        a_point = machine.a * a_presses
        b_point = machine.b * b_presses
        if (a_point + b_point) == machine.prize:
            cost = a_presses * A_COST + b_presses * B_COST
            min_cost = min(min_cost, cost)

    return min_cost if min_cost != float("inf") else 0


def part1():
    machines = parse_data(read_input())
    return sum(determine_cost(machine) for machine in machines)


# It's pretty clear this is the completely incorrect approach,
# but I'll keep it for posterity.
# For part 2, let's try to optimize a linear equation?
# Solving for, essentially:
#   ap * ax + bp * bx = px
#   ap * ay + bp * by = py


def determine_big_cost(machine: Machine) -> int:
    ax, ay = machine.a
    bx, by = machine.b
    px, py = machine.prize

    determinant = ax * by - ay * bx
    numerator_a = px * by - py * bx
    numerator_b = ax * py - ay * px

    if numerator_a % determinant != 0 or numerator_b % determinant != 0:
        # No integer solution exists
        return 0

    a_presses = numerator_a // determinant
    b_presses = numerator_b // determinant

    total_cost = a_presses * A_COST + b_presses * B_COST

    return total_cost


def part2():
    OFFSET = 10000000000000
    machines = parse_data(read_input())
    machines = [machine.offset_prize(OFFSET) for machine in machines]
    return sum(determine_big_cost(machine) for machine in machines)


# pt2 17021305724731227 too high
# pt2 10160000008280962 too high
#     101214869433312


if __name__ == "__main__":
    print(part2())
