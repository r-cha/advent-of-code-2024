import sys
from functools import cache


def read_input():
    if len(sys.argv) == 2:
        with open(sys.argv[1], "r") as f:
            return f.read().strip()
    return sys.stdin.read().strip()


def parse_data(data):
    return (int(c) for c in data.split(" "))


def digits(x):
    return len(str(x))


def split(x):
    s = str(x)
    return int(s[: len(s) // 2]), int(s[len(s) // 2 :])


@cache
def handle_stone(stone):
    if stone == 0:
        return (1,)
    elif digits(stone) % 2 == 0:
        return split(stone)
    else:
        return (stone * 2024,)


@cache
def recursive_blink_x_times(x, data):
    if x == 0:
        return len(data)
    return sum(recursive_blink_x_times(x - 1, handle_stone(stone)) for stone in data)


def part1():
    data = parse_data(read_input())
    return recursive_blink_x_times(25, data)


def part2():
    data = parse_data(read_input())
    return recursive_blink_x_times(75, data)


if __name__ == "__main__":
    print(part2())
