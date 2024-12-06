import enum
import sys
from typing import NamedTuple


def read_input():
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            return f.read().strip()
    return sys.stdin.read().strip()


def is_indexable(r, c, map):
    return (0 <= r < len(map)) and (0 <= c < len(map[0]))


def safe_get(s, index, default=None):
    if 0 <= index < len(s):
        return s[index]
    return default


class Direction(enum.Enum):
    NORTH = "^"
    EAST = ">"
    SOUTH = "v"
    WEST = "<"

    def left(self) -> "Direction":
        match self:
            case Direction.NORTH:
                return Direction.WEST
            case Direction.EAST:
                return Direction.NORTH
            case Direction.SOUTH:
                return Direction.EAST
            case Direction.WEST:
                return Direction.SOUTH

    def right(self) -> "Direction":
        match self:
            case Direction.NORTH:
                return Direction.EAST
            case Direction.EAST:
                return Direction.SOUTH
            case Direction.SOUTH:
                return Direction.WEST
            case Direction.WEST:
                return Direction.NORTH

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


class GuardBase(NamedTuple):
    row: int
    column: int
    direction: Direction


class Guard(GuardBase):
    __slots__ = ()

    def turn(self):
        return Guard(self.row, self.column, self.direction.right())

    def next_index(self) -> tuple[int, int]:
        r, c = self.direction.offset()
        return self.row + r, self.column + c

    def move(self):
        r, c = self.next_index()
        return Guard(r, c, self.direction)

    def look_ahead(self, map: list[str]) -> str | None:
        row, col = self.next_index()
        return safe_get(safe_get(map, row, ""), col)


def parse_map(data: str) -> tuple[list[str], Guard]:
    guard = None
    map: list[str] = []
    for i, row in enumerate(data.split("\n")):
        r = ""
        for j, col in enumerate(row):
            r += col
            if col in Direction:
                guard = Guard(i, j, Direction(col))
        map.append(r)

    assert guard is not None
    return map, guard


def traverse_map(map: list[str], guard: Guard) -> set[tuple[int, int]]:
    visited = set()
    while is_indexable(guard.row, guard.column, map):
        visited.add((guard.row, guard.column))
        ahead_char = guard.look_ahead(map)
        if ahead_char == "#":
            guard = guard.turn()
        guard = guard.move()
    return visited


def part1() -> int:
    """Map out the guard's path and return the number of spaces visited"""
    data = read_input()
    map, guard = parse_map(data)
    visited = traverse_map(map, guard)
    return len(visited)


def debug_print(
    map: list[str],
    guard: Guard,
    visited: set[Guard],
    theoretically_visited: set[Guard] | None = None,
    possible_obstacles: set[tuple[int, int]] | None = None,
):
    class Universe(enum.Enum):
        IN_THEORY = 1
        IN_FACT = 2

    def did_visit(row: int, col: int, dirs: tuple):
        if theoretically_visited and any(
            Guard(row, col, d) in theoretically_visited for d in dirs
        ):
            return Universe.IN_THEORY
        return (
            Universe.IN_FACT
            if any(Guard(row, col, d) in visited for d in dirs)
            else None
        )

    def vertical_visited(row: int, col: int):
        return did_visit(row, col, (Direction.NORTH, Direction.SOUTH))

    def horizontal_visited(row: int, col: int):
        return did_visit(row, col, (Direction.EAST, Direction.WEST))

    for i, row in enumerate(map):
        for j, col in enumerate(row):
            univ = horizontal_visited(i, j)
            unih = vertical_visited(i, j)
            if possible_obstacles and (i, j) in possible_obstacles:
                print("\033[94mO\033[0m", end="")
            elif univ or unih:
                char = "?"
                if univ and unih:
                    char = "+"
                elif univ:
                    char = "-"
                elif unih:
                    char = "|"
                if univ == Universe.IN_THEORY or unih == Universe.IN_THEORY:
                    print("\033[91m" + char + "\033[0m", end="")
                else:
                    print(char, end="")
            elif i == guard.row and j == guard.column:
                print(guard.direction.value, end="")
            else:
                print(col, end="")
        print()
    print()


def add_obstacle(map: list[str], location: tuple[int, int]) -> list[str]:
    row, col = location
    return [
        "".join("#" if r == row and c == col else map[r][c] for c in range(len(map[r])))
        for r in range(len(map))
    ]


def move_ahead(guard: Guard, map: list[str], visited: set[Guard]) -> Guard:
    visited.add(guard)
    ahead_char = guard.look_ahead(map)
    if ahead_char == "#":
        return guard.turn()
    return guard.move()


def check_path_for_loops(
    map: list[str],
    guard: Guard,
    visited: set[Guard],
) -> bool:
    theoretically_visited = set(visited)
    while is_indexable(guard.row, guard.column, map):
        if guard in theoretically_visited:
            return True
        guard = move_ahead(guard, map, theoretically_visited)
    return False


def part2():
    """How many spaces can a new obstacle be placed in that would send the guard into a loop?"""
    data = read_input()
    map, guard = parse_map(data)

    visited: set[Guard] = set()
    possible_obstacles: set[tuple[int, int]] = set()
    while is_indexable(guard.row, guard.column, map):
        if guard.look_ahead(map) not in {"#", None} and check_path_for_loops(
            add_obstacle(map, guard.next_index()),
            Guard(guard.row, guard.column, guard.direction),
            visited,
        ):
            possible_obstacles.add(guard.next_index())
        guard = move_ahead(guard, map, visited)
    debug_print(map, guard, visited, possible_obstacles=possible_obstacles)
    return len(possible_obstacles)


def err(result: int):
    attempts = {
        1614: "strikes me as, perhaps, too high",
        1593: "obviously wrong",
        1591: "way too high",
        1561: "tried this the first time... too high",
        1524: "will still be too high",
        1519: "too high",
        1518: "is the year in which this scenario takes place",
        1415: "is wrong (still)",
        1414: "you can't just subtract 1 and expect it to be right",
        1378: "also wrong",
        1377: "just as wrong as 1378",
        1324: "is inexplicably incorrect",
        1323: "again with the subtracting thing?",
    }
    if result == 6:
        return " \033[1;33m(that's the test data)"
    if result == 4789:
        return " \033[1;33mis the answer to part 1!"
    if result in attempts:
        return f" \033[91m{attempts[result]}"
    elif result > 1519:
        return " \033[91mtoo high"
    return " \033[0;32mcould be it???"


if __name__ == "__main__":
    result = part2()
    print(result, end="")
    print(err(result), end="\033[0m")
    print()
