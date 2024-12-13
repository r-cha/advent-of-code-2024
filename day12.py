import sys


def read_input():
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            return f.read().strip()
    return sys.stdin.read().strip()


def parse_data(input):
    data = {}
    for r, line in enumerate(input.splitlines()):
        for c, cell in enumerate(line):
            data[(r, c)] = cell
    return data


def contiguous_regions(data: dict[tuple[int, int], str]):
    regions = []  # A list of sets of coordinates
    visited = set()
    for coord, cell in data.items():
        if coord in visited:
            continue
        visited.add(coord)
        # Explore adjacent cells to find a region of identical cells
        region = {coord}
        stack = [coord]
        while stack:
            r, c = stack.pop()
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                neighbor = (r + dr, c + dc)
                if data.get(neighbor) == cell and neighbor not in region:
                    stack.append(neighbor)
                    region.add(neighbor)
                    visited.add(neighbor)
        regions.append(region)
    return regions


def score_pt1(region: set[tuple[int, int]]) -> int:
    """A score of a region is its area * its perimeter"""
    # Could probably calculate this for each region as its discovered, but...
    perimeter = 0
    for r, c in region:
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            if (r + dr, c + dc) not in region:
                perimeter += 1
    return len(region) * perimeter


def do_the_thing(score):
    data = parse_data(read_input())
    regions = contiguous_regions(data)
    return sum(score(region) for region in regions)


def part1():
    return do_the_thing(score_pt1)


def number_sides(region: set[tuple[int, int]]) -> int:
    # we'll just iterate horizontally and vertically and count the unmber of unique runs.
    rows = set()
    cols = set()
    for r, c in region:
        rows.add(r)
        cols.add(c)
    minr, minc = min(rows), min(cols)
    maxr, maxc = max(rows), max(cols)

    h_sides = 0
    for r in range(minr, maxr + 1):
        a_run, b_run = False, False
        for c in range(minc, maxc + 1):
            if (r, c) not in region:
                a_run, b_run = False, False
                continue
            if (r - 1, c) not in region:
                if not a_run:
                    h_sides += 1
                    a_run = True
            else:
                a_run = False
            if (r + 1, c) not in region:
                if not b_run:
                    h_sides += 1
                    b_run = True
            else:
                b_run = False
    v_sides = 0
    for c in range(minc, maxc + 1):
        l_run, r_run = False, False
        for r in range(minr, maxr + 1):
            if (r, c) not in region:
                l_run, r_run = False, False
                continue
            if (r, c - 1) not in region:
                if not l_run:
                    v_sides += 1
                    l_run = True
            else:
                l_run = False
            if (r, c + 1) not in region:
                if not r_run:
                    v_sides += 1
                    r_run = True
            else:
                r_run = False
    return h_sides + v_sides


def debug_print(region, data):
    maxr, maxc = 0, 0
    maxr, maxc = list((max(r, maxr), max(c, maxc)) for r, c in data)[-1]
    for r in range(maxr + 1):
        for c in range(maxc + 1):
            if (r, c) in region:
                print("\033[0;31m", end="")
            print(data.get((r, c), " "), end="")
            if (r, c) in region:
                print("\033[0m", end="")
        print()


def score_pt2(region: set[tuple[int, int]]) -> int:
    """A score of a region is its area * its number of sides"""
    sides = number_sides(region)
    area = len(region)
    return area * sides


def part2():
    return do_the_thing(score_pt2)


if __name__ == "__main__":
    print(part2())
