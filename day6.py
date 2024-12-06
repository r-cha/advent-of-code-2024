import enum
import sys


def read_input():
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            return f.read().strip()
    return sys.stdin.read().strip()


def safe_get(s, index, default=None):
    if 0 <= index < len(s):
        return s[index]
    return default


class Direction(enum.Enum):
    NORTH = "^"
    EAST = ">"
    SOUTH = "v"
    WEST = "<"

    def right(self):
        match self:
            case Direction.NORTH:
                return Direction.EAST
            case Direction.EAST:
                return Direction.SOUTH
            case Direction.SOUTH:
                return Direction.WEST
            case Direction.WEST:
                return Direction.NORTH


class Guard:
    def __init__(self, row: int, column: int, direction: Direction) -> None:
        self.row = row
        self.column = column
        self.direction = direction

    def move(self):
        match self.direction:
            case Direction.NORTH:
                self.row -= 1
            case Direction.EAST:
                self.column += 1
            case Direction.SOUTH:
                self.row += 1
            case Direction.WEST:
                self.column -= 1
        return self

    def ahead_index(self) -> tuple[int, int]:
        dir_id_map = {
            Direction.NORTH: (self.row - 1, self.column),
            Direction.EAST: (self.row, self.column + 1),
            Direction.SOUTH: (self.row + 1, self.column),
            Direction.WEST: (self.row, self.column - 1),
        }
        return dir_id_map[self.direction]

    def look_ahead(self, map: list[str]) -> str | None:
        row, col = self.ahead_index()
        return safe_get(safe_get(map, row, ""), col)


def parse_map(data: str) -> tuple[list[str], Guard]:
    guard = None
    map = []
    for i, row in enumerate(data.split("\n")):
        r = ""
        for j, col in enumerate(row):
            r += col
            if col in Direction:
                guard = Guard(i, j, Direction(col))
        map.append(r)

    return map, guard


def traverse_map(map: list[str], guard: Guard) -> set[tuple[int, int]]:
    visited = set()
    while 0 <= guard.row < len(map) and 0 <= guard.column < len(map[0]):
        visited.add((guard.row, guard.column))
        ahead_char = guard.look_ahead(map)
        if ahead_char == "#":
            guard.direction = guard.direction.right()
        guard.move()
    return visited


def part1() -> int:
    """Map out the guard's path and return the number of spaces visited"""
    data = read_input()
    map, guard = parse_map(data)
    visited = traverse_map(map, guard)
    return len(visited)


def add_obstacle(map: list[str], row: int, col: int) -> list[str]:
    return [
        "".join("#" if r == row and c == col else map[r][c] for c in range(len(map[r])))
        for r in range(len(map))
    ]


def debug_print(
    map: list[str],
    guard: Guard,
    visited: set[tuple[int, int, Direction]],
    possible_obstacles: set[tuple[int, int]],
    theoretically_visited: set[tuple[int, int, Direction]] = None,
):
    class Universe(enum.Enum):
        IN_THEORY = 1
        IN_FACT = 2

    def did_visit(row, col, dirs):
        if theoretically_visited and any(
            (row, col, d) in theoretically_visited for d in dirs
        ):
            return Universe.IN_THEORY
        return Universe.IN_FACT if any((row, col, d) in visited for d in dirs) else None

    def vertical_visited(row, col):
        return did_visit(row, col, (Direction.NORTH, Direction.SOUTH))

    def horizontal_visited(row, col):
        return did_visit(row, col, (Direction.EAST, Direction.WEST))

    for i, row in enumerate(map):
        for j, col in enumerate(row):
            if (i, j) in possible_obstacles:
                print("\033[92mO\033[0m", end="")
            elif (uni1 := horizontal_visited(i, j)) and (
                uni2 := vertical_visited(i, j)
            ):
                if uni1 == Universe.IN_THEORY or uni2 == Universe.IN_THEORY:
                    print("\033[91m+\033[0m", end="")
                else:
                    print("+", end="")
            elif uni := horizontal_visited(i, j):
                if uni == Universe.IN_THEORY:
                    print("\033[91m-\033[0m", end="")
                else:
                    print("-", end="")
            elif uni := vertical_visited(i, j):
                if uni == Universe.IN_THEORY:
                    print("\033[91m|\033[0m", end="")
                else:
                    print("|", end="")
            elif i == guard.row and j == guard.column:
                print(guard.direction.value, end="")
            else:
                print(col, end="")
        print()
    print()


def move_ahead(guard, map, visited):
    visited.add((guard.row, guard.column, guard.direction))
    ahead_char = guard.look_ahead(map)
    while ahead_char == "#":
        guard.direction = guard.direction.right()
        visited.add((guard.row, guard.column, guard.direction))
        ahead_char = guard.look_ahead(map)
    guard.move()


def check_path_for_loops(
    map: list[str],
    guard: Guard,
    visited: set[tuple[int, int, Direction]],
) -> bool:
    """Shortcut a full traversal by checking if the guard is in a loop."""
    theoretically_visited = set(visited)
    while 0 <= guard.row < len(map) and 0 <= guard.column < len(map[0]):
        if (guard.row, guard.column, guard.direction) in theoretically_visited:
            debug_print(map, guard, visited, set(), theoretically_visited-visited)
            input()
            return True
        move_ahead(guard, map, theoretically_visited)
    return False


def part2():
    """How many spaces can a new obstacle be placed in that would send the guard into a loop?"""
    data = read_input()
    map, guard = parse_map(data)

    visited = set()  # with direction
    possible_obstacles = set()  # Just (row, col) tuples
    while 0 <= guard.row < len(map) and 0 <= guard.column < len(map[0]):
        # Imagine a world where there is an obstacle in the way.
        # If that world loops, then the obstacle is a candidate.
        if (
            guard.ahead_index() not in possible_obstacles
            and check_path_for_loops(
                add_obstacle(map, *guard.ahead_index()),
                Guard(guard.row, guard.column, guard.direction.right()),
                visited,
            )
        ):
            possible_obstacles.add(guard.ahead_index())
        move_ahead(guard, map, visited)
    return len(possible_obstacles)


# 1561 too high
# 1519 too high
# 1524 will still be too high
# 1591 way too high
# 1593 obsiously wrong
# 1415 is wrong
# 1378 also wrong (2 hrs later: still wrong)
# 1614 strikes me as, perhaps, too high


if __name__ == "__main__":
    print(part2())
