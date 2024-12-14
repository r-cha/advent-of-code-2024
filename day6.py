import enum
import sys
from typing import NamedTuple, Sequence, TypeVar


def read_input() -> str:
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            return f.read().strip()
    return sys.stdin.read().strip()


def inbounds(r: int, c: int, lab: list[Sequence]):
    return (0 <= r < len(lab)) and (0 <= c < len(lab[0]))


T = TypeVar("T")


def safe_get(s: Sequence[T], index: int, default: T | None = None) -> T | None:
    if 0 <= index < len(s):
        return s[index]
    return default


class Direction(enum.Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def left(self) -> "Direction":
        return Direction((self.value - 1) % 4)

    def right(self) -> "Direction":
        return Direction((self.value + 1) % 4)

    def offset(self) -> tuple[int, int]:
        match self:
            case Direction.NORTH:
                return (-1, 0)
            case Direction.EAST:
                return (0, 1)
            case Direction.SOUTH:
                return (1, 0)
            case Direction.WEST:
                return (0, -1)


class Guard(NamedTuple):
    row: int
    column: int
    direction: Direction

    def turn(self):
        return Guard(self.row, self.column, self.direction.right())

    def next_index(self) -> tuple[int, int]:
        r, c = self.direction.offset()
        return self.row + r, self.column + c

    def move(self):
        r, c = self.next_index()
        return Guard(r, c, self.direction)

    def look_ahead(self, lab: list[str]) -> str | None:
        row, col = self.next_index()
        return safe_get(safe_get(lab, row, ""), col)


def parse_lab(data: str) -> tuple[list[str], Guard]:
    guard = None
    lab: list[str] = []
    for i, row in enumerate(data.split("\n")):
        r = ""
        for j, col in enumerate(row):
            r += col
            if col == "^":
                guard = Guard(i, j, Direction.NORTH)
        lab.append(r)

    assert guard is not None
    return lab, guard


def traverse_lab(lab: list[str], guard: Guard) -> set[tuple[int, int]]:
    visited = set()
    while inbounds(guard.row, guard.column, lab):
        visited.add((guard.row, guard.column))
        ahead_char = guard.look_ahead(lab)
        if ahead_char == "#":
            guard = guard.turn()
        guard = guard.move()
    return visited


def part1() -> int:
    """Map out the guard's path and return the number of spaces visited"""
    data = read_input()
    lab, guard = parse_lab(data)
    visited = traverse_lab(lab, guard)
    return len(visited)


Point = tuple[int, int]
Lab = dict[Point, str]


def parse_data(input: str) -> Lab:
    start = None
    lab = {}
    for r, line in enumerate(input.splitlines()):
        for c, char in enumerate(line):
            lab[(r, c)] = char
            if char == "^":
                start = (r, c)
    assert start is not None
    return lab, start


def move(lab: Lab, position: Point, direction: Point, obstacle: Point | None = None):
    dr, dc = direction
    next_position = (position[0] + dr, position[1] + dc)
    if lab.get(next_position) == "#" or next_position == obstacle:
        return move(lab, position, (dc, -dr), obstacle)
    return next_position, direction


def traverse(lab: Lab, start: Point, obstacle: Point | None = None):
    visited = set()
    path = set()
    location = start
    direction = (-1, 0)
    while location in lab:
        if (location, direction) in path:
            return True
        visited.add(location)
        path.add((location, direction))
        location, direction = move(lab, location, direction, obstacle)
    return visited


def part2_revisited():
    lab, start = parse_data(read_input())
    path = traverse(lab, start)
    return sum(traverse(lab, start, obs) is True for obs in path)


def err(result: int):
    attempts = {
        1614: "strikes me as, perhaps, too high",
        1593: "obviously wrong",
        1591: "way too high",
        1561: "was the first attempt... too high",
        1524: "is still too high",
        1519: "also too high",
        1518: "is the year in which this scenario takes place",
        1415: "is wrong (still)",
        1414: "you can't just subtract 1 and expect it to be right",
        1378: "also wrong",
        1377: "just as wrong as 1378",
        1324: "is inexplicably incorrect",
        1323: "again with the subtracting thing?",
        1278: "not even reasonable",
    }
    if result == 6:
        return " \033[1;33m(that's the test data)"
    elif result == 4789:
        return " \033[1;33mis the answer to part 1!"
    elif result in attempts:
        return f" \033[91m{attempts[result]}"
    elif result > 1519:
        return " \033[91mtoo high"
    elif result == 1304:
        return " \033[1;32mthat's it!"
    return " \033[0;32mcould be it???"


if __name__ == "__main__":
    result = part2_revisited()
    print(result, end="")
    print(err(result), end="\033[0m")
    print()
