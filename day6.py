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


def debug_print(
    lab: list[str],
    visited: set[Guard],
    theoretically_visited: set[Guard] | None = None,
    possible_obstacles: set[tuple[int, int]] | None = None,
):
    class Universe(enum.Enum):
        THEORY = 1
        FACT = 2

    def did_visit(row: int, col: int, dirs: tuple):
        if theoretically_visited and any(
            Guard(row, col, d) in theoretically_visited for d in dirs
        ):
            return Universe.THEORY
        return (
            Universe.FACT if any(Guard(row, col, d) in visited for d in dirs) else None
        )

    def vertical_visited(row: int, col: int):
        return did_visit(row, col, (Direction.NORTH, Direction.SOUTH))

    def horizontal_visited(row: int, col: int):
        return did_visit(row, col, (Direction.EAST, Direction.WEST))

    for i, row in enumerate(lab):
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
                if univ == Universe.THEORY or unih == Universe.THEORY:
                    print("\033[91m" + char + "\033[0m", end="")
                else:
                    print(char, end="")
            else:
                print(col, end="")
        print()
    print()


def move_ahead(
    guard: Guard,
    lab: list[str],
    visited: set[Guard],
    obstacle: tuple[int, int] | None = None,
) -> Guard:
    """Visit the guard's space, then take an action (move or turn)"""
    visited.add(guard)
    ahead_char = guard.look_ahead(lab)
    if ahead_char == "#" or (obstacle and guard.next_index() == obstacle):
        return guard.turn()
    return guard.move()


def check_path_for_loops(
    lab: list[str],
    guard: Guard,
    visited: set[Guard],
    obstacle: tuple[int, int] | None,
) -> bool:
    theoretically_visited = set(visited)
    while inbounds(guard.row, guard.column, lab):
        if guard in theoretically_visited:
            return True
        guard = move_ahead(guard, lab, theoretically_visited, obstacle)
    return False


def part2():
    """How many spaces can a new obstacle be placed in that would send the guard into a loop?"""
    data = read_input()
    lab, guard = parse_lab(data)
    home = (guard.row, guard.column)

    visited: set[Guard] = set()
    possible_obstacles: set[tuple[int, int]] = set()
    while inbounds(guard.row, guard.column, lab):
        next_index = guard.next_index()
        if (
            guard.look_ahead(lab) not in {"#", None}  # Must be in bounds + not occupied
            and next_index not in possible_obstacles  # Skip already checked obstacles
            and next_index != home  # Not allowed, also not useful, but just in case
            and check_path_for_loops(
                lab,
                Guard(guard.row, guard.column, guard.direction.right()),
                visited,
                next_index,
            )
        ):
            possible_obstacles.add(next_index)
        guard = move_ahead(guard, lab, visited)
    debug_print(lab, visited, possible_obstacles=possible_obstacles)
    return len(possible_obstacles)


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
    return " \033[0;32mcould be it???"


if __name__ == "__main__":
    result = part2()
    print(result, end="")
    print(err(result), end="\033[0m")
    print()
