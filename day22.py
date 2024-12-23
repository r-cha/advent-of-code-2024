import sys
from collections import defaultdict
from functools import cache


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


def get_nth(start_value, n):
    secret = start_value
    for _ in range(n):
        secret = generate_next(secret)
    return secret


def part1():
    values = parse_input(read_input())
    return sum(get_nth(value, 2000) for value in values)


def generate_n(start_value, n):
    secret = start_value
    for _ in range(n):
        secret = generate_next(secret)
        yield secret


def calculate_price(secret):
    return secret % 10


def part2():
    start_values = parse_input(read_input())
    secrets = {
        start_value: [n for n in generate_n(start_value, 2000)]
        for start_value in start_values
    }

    def price_at(start_value, n):
        return calculate_price(secrets[start_value][n])

    @cache
    def diff_at(start_value, n):
        if n == 0:
            return calculate_price(start_value)
        return price_at(start_value, n) - price_at(start_value, n - 1)

    # The most naive possible approach:
    # For each unique series of 4 values (overlapping),
    # calculate the sell price at the first occurence of that series.
    profits_per_start = {
        sv: {} for sv in start_values
    }  # maps start value to a map of 4-diff tuple to the profit by selling at that point.
    for sv in start_values:
        print(f"Calculating profits for {sv}")
        for i in range(3, len(secrets[sv])):
            ds = tuple(diff_at(sv, i + j) for j in range(-3, 1))
            if ds in profits_per_start[sv]:
                continue
            profits_per_start[sv][ds] = price_at(sv, i)

    # Finally, find the key (d1, d2, d3, d4) that maximizes the profit across all start values.
    def all_diffs():
        d = set()
        for sv in start_values:
            for ds in profits_per_start[sv]:
                d.add(ds)
        return d

    def profit(ds):
        return sum(profits_per_start[sv].get(ds, 0) for sv in start_values)

    all_sequences = all_diffs()
    print(len(all_sequences))
    best_diff = max(all_sequences, key=profit)
    print(best_diff)
    return profit(best_diff)


if __name__ == "__main__":
    print(part2())
