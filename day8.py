import sys
from collections import defaultdict
from itertools import combinations
from types import new_class


def read_input() -> str:
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            return f.read().strip()
    return sys.stdin.read().strip()


def parse_input(data: str) -> dict[str, list[tuple[int, int]]]:
    """Get a dict mapping antenna names to their locations."""
    antennae = defaultdict(list)
    lines = data.splitlines()
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == ".":
                continue
            antennae[char].append((i, j))
    return antennae


def taxicab_distances(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return a[0] - b[0], a[1] - b[1]


def debug_print(data, antinodes):
    lines = data.splitlines()
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if (i, j) in antinodes:
                print("#", end="")
            else:
                print(char, end="")
        print()


def calculate_antinodes(locs: list[tuple[int, int]]) -> set[tuple[int, int]]:
    """
    > An antinode occurs at any point that is perfectly in line with two antennas of the same frequency
    > - but only when one of the antennas is twice as far away as the other.
    > This means that for any pair of antennas with the same frequency,
    > there are two antinodes, one on either side of them.
    """
    antinodes = set()
    # For every pair of distances, calculate the distance between them
    # and save the two points that same distance on either side of the pair.
    for a, b in combinations(locs, 2):
        x_dist, y_dist = taxicab_distances(a, b)
        pt1 = (a[0] + x_dist, a[1] + y_dist)
        pt2 = (b[0] - x_dist, b[1] - y_dist)
        antinodes.add(pt1)
        antinodes.add(pt2)
    return antinodes


def part1() -> int:
    input = read_input()
    lines = input.splitlines()
    data = parse_input(input)
    antinodes = set()
    for locs in data.values():
        print(locs)
        new_antinodes = calculate_antinodes(locs)
        debug_print(input, new_antinodes)
        antinodes |= new_antinodes
    # Remove points outside the grid
    antinodes = {
        loc
        for loc in antinodes
        if 0 <= loc[0] < len(lines) and 0 <= loc[1] < len(lines[0])
    }
    return len(antinodes)


def calculate_antinodes2(
    locs: list[tuple[int, int]], rows: int, cols: int
) -> set[tuple[int, int]]:
    antinodes = set()
    for a, b in combinations(locs, 2):
        antinodes.add(a)
        antinodes.add(b)
        x_dist, y_dist = taxicab_distances(a, b)
        x, y = a
        while 0 <= x < rows and 0 <= y < cols:
            x += x_dist
            y += y_dist
            if 0 <= x < rows and 0 <= y < cols:
                antinodes.add((x, y))
        x, y = b
        while 0 <= x < rows and 0 <= y < cols:
            x -= x_dist
            y -= y_dist
            if 0 <= x < rows and 0 <= y < cols:
                antinodes.add((x, y))
    return antinodes


def part2() -> int:
    input = read_input()
    lines = input.splitlines()
    data = parse_input(input)

    antinodes = set()
    for antenna, locs in data.items():
        new_antinodes = calculate_antinodes2(locs, len(lines), len(lines[0]))
        debug_print(input, new_antinodes)
        antinodes |= new_antinodes
    return len(antinodes)


if __name__ == "__main__":
    result = part2()
    print(result)
