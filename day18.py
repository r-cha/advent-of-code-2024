import sys
import heapq
from itertools import product


def read_input():
    with open(sys.argv[1]) as f:
        return f.read().strip()


def parse_input(data):
    positions = []
    for row in data.splitlines():
        t = tuple(map(int, row.split(",")))
        positions.append(t)
    return positions


def debug_print(memory_space, start, end, path, max_dim):
    for y in range(max_dim + 1):
        for x in range(max_dim + 1):
            if (x, y) == start:
                print("S", end="")
            elif (x, y) == end:
                print("E", end="")
            elif (x, y) in path:
                print("\033[91mo\033[0m", end="")
            elif (x, y) in memory_space:
                print(".", end="")
            else:
                print("#", end="")
        print()
    print()


def find_paths(race, start, end):
    # (cost, current_position, path)
    pq = [(0, start, [])]
    visited = set()

    while pq:
        cost, current, path = heapq.heappop(pq)

        if current in visited:
            continue
        visited.add(current)

        if current == end:
            return cost

        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            next_pos = (current[0] + dx, current[1] + dy)
            if next_pos in race | {end} and next_pos not in visited:
                new_path = path + [next_pos]
                new_cost = cost + 1
                heapq.heappush(pq, (new_cost, next_pos, new_path))


def populate_grid(max_dimension, positions):
    space = set((x, y) for x, y in product(range(max_dimension+1), repeat=2))
    return space - positions


def part1():
    max_dim = 70
    bytes_to_process = 1024  # Spent way too long remembering that I don't include every single byte 😅
    positions = parse_input(read_input())
    memory_space = populate_grid(max_dim, set(positions[:bytes_to_process]))
    min_cost = find_paths(memory_space, (0, 0), (max_dim, max_dim))
    debug_print(memory_space, (0, 0), (max_dim, max_dim), set(), max_dim)
    return min_cost


def bs(arr, condition, start_idx=0):
    """search arr for index where condition(id) becomes false"""
    low, mid, high = start_idx, 0, len(arr) - 1
    while low <= high:
        mid = (high + low) // 2
        # If condition holds, search the right side
        if condition(mid):
            low = mid + 1
        else:
            high = mid - 1
    return mid


def is_possible(positions, max_dim):
    memory_space = populate_grid(max_dim, set(positions))
    min_cost = find_paths(memory_space, (0, 0), (max_dim, max_dim))
    return min_cost is not None


def part2():
    max_dim = 70
    bytes_to_process = 1024
    positions = parse_input(read_input())
    # binary search over the range of positions to find the first invalid path
    idx = bs(positions, lambda id: is_possible(positions[:id], max_dim), bytes_to_process)
    return positions[idx-1]


if __name__ == "__main__":
    print(part2())
