import re
import sys
from math import prod
from typing import NamedTuple


def read_input():
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            return f.read().strip()
    return sys.stdin.read().strip()


class Vector(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, n: int):
        return Vector(self.x * n, self.y * n)

    def __mod__(self, other):
        return Vector(self.x % other.x, self.y % other.y)


class Robot(NamedTuple):
    position: Vector
    direction: Vector


def parse_data(input) -> list[Robot]:
    robots = []
    for line in input.splitlines():
        px, py, vx, vy = re.findall(r"-?\d+", line)
        robots.append(Robot(Vector(int(px), int(py)), Vector(int(vx), int(vy))))
    return robots


def robot_after_x_seconds(robot: Robot, seconds: int, max_v: Vector) -> Robot:
    unwrapped_position = (robot.position + (robot.direction * seconds)) % max_v
    return Robot(unwrapped_position, robot.direction)


def on_the_center(position: Vector, max_v: Vector) -> bool:
    return position.x == max_v.x // 2 or position.y == max_v.y // 2


def quadrant_counts(robots: list[Robot], max_v: Vector) -> list[int]:
    """
    > To determine the safest area, count the number of robots in each quadrant.
    > Robots that are exactly in the middle (horizontally or vertically) don't count as being in any quadrant.
    """
    counts = [0, 0, 0, 0]
    for robot in robots:
        if on_the_center(robot.position, max_v):
            continue
        elif robot.position.x < max_v.x // 2:
            if robot.position.y < max_v.y // 2:
                counts[0] += 1
            else:
                counts[1] += 1
        else:
            if robot.position.y < max_v.y // 2:
                counts[2] += 1
            else:
                counts[3] += 1
    print(counts)
    return counts


def debug_print(robots: list[Robot], max_v: Vector):
    for y in range(max_v.y):
        for x in range(max_v.x):
            if on_the_center(Vector(x, y), max_v):
                print(" ", end="")
            elif any(robot.position == Vector(x, y) for robot in robots):
                print("#", end="")
            else:
                print(".", end="")
        print()


def part1():
    seconds = 100
    max_v = Vector(101, 103)
    robots = parse_data(read_input())
    moved_robots = [robot_after_x_seconds(robot, seconds, max_v) for robot in robots]
    debug_print(moved_robots, max_v)
    return prod(quadrant_counts(moved_robots, max_v))


def eff_debug_print(robots: list[Robot], max_v: Vector):
    robots_positions = {robot.position for robot in robots}
    for y in range(max_v.y):
        for x in range(max_v.x):
            if Vector(x, y) in robots_positions:
                print("#", end="")
            else:
                print(".", end="")
        print()


def woven_series():
    """
    Empirically, I checked out the first ~700 values and saw some that stood out.
    Inspecting their indices, I saw a "woven" pattern (not sure the formal term?).
    > 83+101n
    > 266+103m
    If I find where the two sequences intersect, I can just get that value directly...
    But it's late at night and I literally cannot wrap my head around this simple math.
    Instead, I'll generate the next value, monotonically increasing, and check each picture manually.
    """
    n = 0
    m = 0
    while True:
        a = 83 + 101 * n
        b = 266 + 103 * m
        if a < b:
            yield a
            n += 1
        else:
            yield b
            m += 1


def part2_manual():
    max_v = Vector(101, 103)
    robots = parse_data(read_input())
    seconds = 0
    for seconds in woven_series():
        print("SECONDS:", seconds)
        moved_robots = [
            robot_after_x_seconds(robot, seconds, max_v) for robot in robots
        ]
        eff_debug_print(moved_robots, max_v)
        stop = input()
        if stop == "q":
            break
    return seconds


# Researching the relatinship between these sequences and the answer,
# I learned of the Chinese Remainder Theorem.
# Let's apply it here for posterity.


def egcd(a, b):
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = egcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y


def crt(mods, rems):
    s = 0
    p = prod(mods)
    for m, r in zip(mods, rems):
        q = p // m
        gcd, x, y = egcd(q, m)
        s += r * x * q
    return s % p


def part2():
    max_v = Vector(101, 103)
    robots = parse_data(read_input())
    mods = [101, 103]
    rems = [83, 266]  # Where would I even get these without the manual approach?
    r = crt(mods, rems)
    eff_debug_print([robot_after_x_seconds(robot, r, max_v) for robot in robots], max_v)
    return r


if __name__ == "__main__":
    print(part2())
