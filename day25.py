import sys


def read_input():
    with open(sys.argv[1]) as f:
        return f.read().strip()


def parse_input(data):
    blocks = [line.splitlines() for line in data.split("\n\n")]
    locks, keys = [], []
    for block in blocks:
        if block[0][0] == "#":
            heights = {}
            for y, row in enumerate(block):
                for x, char in enumerate(row):
                    if char == "." and x not in heights:
                        heights[x] = y - 1
            locks.append(
                tuple(
                    height for _, height in sorted(heights.items(), key=lambda x: x[0])
                )
            )
        else:
            heights = {}
            for y, row in enumerate(reversed(block)):
                for x, char in enumerate(row):
                    if char == "." and x not in heights:
                        heights[x] = y - 1
            keys.append(
                tuple(
                    height for _, height in sorted(heights.items(), key=lambda x: x[0])
                )
            )
    return locks, keys


def can_match(lock, key):
    return all(lock[i] + key[i] < 6 for i in range(5))


def find_matches(locks, keys):
    matches = 0
    for lock in locks:
        for key in keys:
            if can_match(lock, key):
                matches += 1

    return matches


def part1():
    locks, keys = parse_input(read_input())
    return find_matches(locks, keys)


if __name__ == "__main__":
    print(part1())
