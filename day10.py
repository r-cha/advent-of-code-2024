import sys
from collections import defaultdict


def read_input():
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            return f.read().strip()
    return sys.stdin.read().strip()


Topo = dict[tuple[int, int], int]


def parse_data(input: str) -> Topo:
    return {
        (x, y): int(cell)
        for y, row in enumerate(input.splitlines())
        for x, cell in enumerate(row)
    }


def debug_print(data: Topo, trail: list[tuple[int, int]]):
    max_x, max_y = (
        max(data, key=lambda pt: pt[0])[0],
        max(data, key=lambda pt: pt[1])[1],
    )
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            cell = data[(x, y)]
            if (x, y) in trail:
                print(f"\033[91m{cell}\033[0m", end="")
            else:
                print(cell, end="")
        print()


def find_trailheads(data: Topo):
    """Given a topo map data, find all the 0's."""
    return [loc for loc, cell in data.items() if cell == 0]


def forge_trails(pt, data, trails):
    """
    Given a point pt and a topo map data, return all trails from pt to 9 that are valid.
    Parameter trails is a dictionary of points to trails.

    > ... A hiking trail is any path that starts at height 0, ends at height 9,
    > and always increases by a height of exactly 1 at each step.
    > Hiking trails never include diagonal steps - only up, down, left, or right.

    The return value should be a list of trails, where each trail is a list of points.
    """
    # If pt is 9, return itself.
    if data[pt] == 9:
        return [[pt]]
    # If pt is already in trails, return it.
    if pt in trails:
        return trails[pt]
    # Otherwise, forge some new trails.
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        x, y = pt
        if (x + dx, y + dy) in data:
            if data[x + dx, y + dy] == data[x, y] + 1:
                new_trails = forge_trails((x + dx, y + dy), data, trails)
                trails[pt] += [[pt] + trail for trail in new_trails]
    return trails[pt]


def score_trailhead(trailhead, trails, data):
    """
    > A trailhead's score is the number of unique 9-height positions reachable from that trailhead via a hiking trail.
    """
    unique_nines = {trail[-1] for trail in trails[trailhead] if data[trail[-1]] == 9}
    # print(f"{trailhead}: {len(unique_nines)}")
    return len(unique_nines)


def rate_trailhead(trailhead, trails, data):
    """
    > A trailhead's rating is the number of distinct hiking trails which begin at that trailhead.
    (and end at a 9-height position)
    """
    return len(list(trail for trail in trails[trailhead] if data[trail[-1]] == 9))


def do_the_thing(score_func):
    """
    1. Find every trail to 9 from every point on the grid.
    2. Find every trailhead (0) that leads to a 9.
    3. Sum the scores of those trails.
    """
    data = parse_data(read_input())
    trailheads = find_trailheads(data)
    trails_start = defaultdict(list)
    trails = {pt: forge_trails(pt, data, trails_start) for pt in trailheads}
    # print(trails)
    # [[debug_print(data, trail) for trail in trails[th]] for th in trailheads]
    return sum(score_func(th, trails, data) for th in trailheads)


def part1():
    """
    > What is the sum of the scores of all trailheads on your topographic map?
    """
    return do_the_thing(score_trailhead)


def part2():
    """
    > What is the sum of the ratings of all trailheads on your topographic map?
    """
    return do_the_thing(rate_trailhead)


if __name__ == "__main__":
    print(part2())
