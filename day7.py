import operator
import sys
from itertools import product


def read_input() -> str:
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            return f.read().strip()
    return sys.stdin.read().strip()


def parse_input(data: str) -> list[tuple[int, list[int]]]:
    return [
        (int(x), [int(y) for y in xs.split(" ")])
        for x, xs in [x.split(": ") for x in data.splitlines()]
    ]


def debug_print(answer: int, row: list[int], ops: list):
    print(f"{answer} = {row[0]}", end="")
    for op, b in zip(ops, row[1:]):
        o = "+" if op == operator.add else "*"
        print(f" {o} {b}", end="")
    print()


def con(a: int, b: int) -> int:
    """
    > The concatenation operator (||) combines the digits from its left and right inputs into a single number.
    > For example, 12 || 345 would become 12345
    """

    return a * 10 ** len(str(b)) + b


def possible_input(row: tuple[int, list[int]], ops=[]) -> bool:
    for combo in product([operator.add, operator.mul] + ops, repeat=len(row[1]) - 1):
        v = row[1][0]
        for op, b in zip(combo, row[1][1:]):
            v = op(v, b)
        if v == row[0]:
            # debug_print(v, row[1], combo)
            return True
    return False


def part1():
    data = parse_input(read_input())
    return sum(row[0] for row in data if possible_input(row))


def part2():
    data = parse_input(read_input())
    return sum(row[0] for row in data if possible_input(row, [con]))


def check_attempts1(result):
    if result == 492383931650959:
        return " correct! (part 2)"
    if result == 5837374519342:
        return " correct! (part 1)"
    if result <= 5751665305499:
        return " too low"
    return " ?"


if __name__ == "__main__":
    result = part2()
    print(result, end="")
    print(check_attempts1(result))
