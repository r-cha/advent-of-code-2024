import sys
from typing import Counter


def read_input() -> str:   
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            data = f.read()
    else:
        data = sys.stdin.read()

    return data


def parse_lists(data: str) -> tuple[list[int], list[int]]:
    l1, l2 = [], []
    for line in data.splitlines():
        v1, v2 = map(int, line.split())
        l1.append(v1)
        l2.append(v2)

    return l1, l2


def distance_between_lists(l1: list[int], l2: list[int]) -> int:
    return sum(abs(a - b) for a, b, in zip(sorted(l1), sorted(l2)))


def part_1():
    print("day 1")
    data = read_input()
    print("data: ", len(data))
    l1, l2 = parse_lists(data)
    print("parsed: " , len(l1), len(l2))
    d = distance_between_lists(l1, l2)
    print("Answer: ", d)


def similarity(left: list[int], right: list[int]) -> int:
    frequency = Counter(right)
    return sum(v * frequency[v] for v in left)


def part_2():
    print("part 2")
    data = read_input()
    print("data: ", len(data))
    left, right = parse_lists(data)
    print("parsed: ", len(left), len(right))
    s = similarity(left, right)
    print("Answer: ", s)


if __name__ == "__main__":
    part_2()

