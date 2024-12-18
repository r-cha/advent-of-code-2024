from collections import Counter
import heapq
import sys


def read_input() -> str:
    with open(sys.argv[1]) as f:
        return f.read().strip()


def parse_input(data):
    race = set()
    start = None
    end = None
    for y, line in enumerate(data.splitlines()):
        for x, char in enumerate(line):
            match char:
                case ".":
                    race.add((x, y))
                case "S":
                    start = (x, y)
                case "E":
                    end = (x, y)
    assert start is not None
    assert end is not None
    return race, start, end


def debug_print(race, start, end, path):
    pathset = set(path)
    maxx, maxy = max(k[0] for k in race), max(k[1] for k in race)
    for y in range(maxy + 1):
        for x in range(maxx + 1):
            if (x, y) == start:
                print("S", end="")
            elif (x, y) == end:
                print("E", end="")
            elif (x, y) in pathset:
                print("\033[91mo\033[0m", end="")
            elif (x, y) in race:
                print(".", end="")
            else:
                print("#", end="")
        print()
    print()


def find_paths(race, start, end):
    pq = [
        (0, (start[0] - 1, start[1]), start, [])
    ]  # (cost, prev_position, current_position, path)
    counter = Counter()
    min_cost = float("inf")

    while pq:
        cost, previous, current, path = heapq.heappop(pq)

        if counter[current] > 10:
            continue
        counter[current] += 1

        if current == end:
            min_cost = min(min_cost, cost)
            print(cost)
            # debug_print(race, start, end, path)
            continue

        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            prev_dir = (current[0] - previous[0], current[1] - previous[1])
            if (dx, dy) == (-prev_dir[0], -prev_dir[1]):
                continue
            next_pos = (current[0] + dx, current[1] + dy)
            if next_pos in race | {end}:
                new_path = path + [next_pos]
                is_turn = (dx, dy) != prev_dir
                new_cost = cost + 1 + is_turn * 1000
                heapq.heappush(pq, (new_cost, current, next_pos, new_path))

    return min_cost


def part1():
    race, start, end = parse_input(read_input())
    min_cost = find_paths(race, start, end)
    return min_cost


if __name__ == "__main__":
    print(part1())
