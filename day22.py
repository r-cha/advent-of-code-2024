import sys


def read_input():
    with open(sys.argv[1]) as f:
        return f.read().strip()


def parse_input(data):
    return [int(x) for x in data.splitlines()]


def mix(value, secret):
    return value ^ secret


def prune(secret):
    return secret & (2**24 - 1)


def generate_next(secret):
    secret = prune(mix(secret << 6, secret))
    secret = prune(mix(secret >> 5, secret))
    secret = prune(mix(secret << 11, secret))
    return secret


def generate_nth(start_value, n):
    secret = start_value
    for _ in range(n):
        secret = generate_next(secret)
    return secret


def part1():
    values = parse_input(read_input())
    return sum(generate_nth(value, 2000) for value in values)


if __name__ == "__main__":
    print(part1())
