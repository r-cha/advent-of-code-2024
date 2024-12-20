from collections import defaultdict, Counter
import sys


def read_input():
    with open(sys.argv[1]) as f:
        return f.read().strip()


def debug_print(track, start, end, shortcuts):
    maxx, maxy = max(x for x, y in track), max(y for x, y in track)
    for y in range(maxy + 2):
        for x in range(maxx + 2):
            if (x, y) == start:
                print("S", end="")
            elif (x, y) == end:
                print("E", end="")
            elif (x, y) in shortcuts:
                print("\033[91m#\033[0m", end="")
            elif (x, y) in track:
                print(".", end="")
            else:
                print("#", end="")
        print()


def parse_input(input):
    start, end = None, None
    data = set()
    for y, row in enumerate(input.splitlines()):
        for x, cell in enumerate(row):
            if cell == ".":
                data.add((x, y))
            elif cell == "S":
                start = (x, y)
            elif cell == "E":
                end = (x, y)
    return data, start, end


def score_cells(racetrack, start, end):
    """Return the score of each cell in the racetrack."""
    score = {start: 0}
    queue = [start]
    while queue:
        x, y = queue.pop(0)
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_loc = x + dx, y + dy
            if (new_loc in racetrack or new_loc == end) and new_loc not in score:
                score[new_loc] = score[(x, y)] + 1
                queue.append(new_loc)
    return score


def find_shortcuts(scores, cheat_length=2):
    """
    Return all possible shortcuts on the track:
    points adjacent to two points on the racetrack in the same axis
    """
    shortcuts = defaultdict(
        lambda: float("inf")
    )  # maps a shortcut to the picoseconds it saves
    for x, y in sorted(scores, key=lambda p: scores[p]):
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            shortcut = x + dx, y + dy
            next_point = x + (cheat_length * dx), y + (cheat_length * dy)
            if shortcut not in scores and next_point in scores:
                diff = scores[next_point] - scores[(x, y)] - cheat_length
                if diff > 0:
                    shortcuts[shortcut] = min(shortcuts[shortcut], diff)
    return shortcuts


# 427 too low


def part1():
    data, start, end = parse_input(read_input())
    scores = score_cells(data, start, end)
    shortcuts = find_shortcuts(scores)
    cheats_per_score = Counter(shortcuts.values())
    debug_print(data, start, end, {s for s in shortcuts if shortcuts[s] >= 100})
    return sum(cheats for score, cheats in cheats_per_score.items() if score >= 100)


if __name__ == "__main__":
    print(part1())
