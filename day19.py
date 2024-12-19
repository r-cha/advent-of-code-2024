import sys


def read_input():
    with open(sys.argv[1]) as f:
        return f.read().strip()


def parse_input(data):
    patternstr, designstr = data.split("\n\n")
    patterns = patternstr.split(", ")
    designs = designstr.splitlines()
    return patterns, designs


def ways_to_make(design, patterns):
    """Return the number of ways to make the design using the given patterns."""
    n = len(design)
    cache = [0] * (n + 1)
    cache[0] = 1  # One way to compose an empty string

    for i in range(1, n + 1):
        for p in patterns:
            plen = len(p)
            if plen <= i and design[i - plen : i] == p:
                cache[i] += cache[i - plen]

    return cache[n]


def part1():
    patterns, designs = parse_input(read_input())
    return sum(bool(ways_to_make(d, patterns)) for d in designs)


def part2():
    patterns, designs = parse_input(read_input())
    return sum(ways_to_make(d, patterns) for d in designs)


if __name__ == "__main__":
    print(part2())
