import sys
from enum import Enum
from functools import cache


def read_input():
    with open(sys.argv[1]) as f:
        return f.read().strip()


def parse_input(data):
    return data.splitlines()


directional_keypad = {
    "^": (1, 0),
    "A": (2, 0),
    "<": (0, 1),
    "v": (1, 1),
    ">": (2, 1),
}

numeric_keypad = {
    "7": (0, 0),
    "8": (1, 0),
    "9": (2, 0),
    "4": (0, 1),
    "5": (1, 1),
    "6": (2, 1),
    "1": (0, 2),
    "2": (1, 2),
    "3": (2, 2),
    "0": (1, 3),
    "A": (2, 3),
}


class Keypad(Enum):
    DIRECTIONS = 1
    NUMERIC = 2

    def to_keypad(self):
        if self == Keypad.DIRECTIONS:
            return directional_keypad
        else:
            return numeric_keypad


@cache
def directions(fr, to, keypad):
    """
    Give the sequence of directions to go from one point to another.
    """
    from_x, from_y = keypad.to_keypad()[fr]
    to_x, to_y = keypad.to_keypad()[to]
    dx = to_x - from_x
    dy = to_y - from_y
    seq = ""
    v = "v" * dy if dy > 0 else "^" * abs(dy)
    h = ">" * dx if dx > 0 else "<" * abs(dx)
    # Out-of-bounds avoidance rules
    if keypad == Keypad.NUMERIC and from_y == 3 and to_x == 0:
        seq = v + h
    elif keypad == Keypad.NUMERIC and from_x == 0 and to_y == 3:
        seq = h + v
    elif keypad == Keypad.DIRECTIONS and from_x == 0:
        seq = h + v
    elif keypad == Keypad.DIRECTIONS and to_x == 0:
        seq = v + h
    # General case
    elif dx < 0:
        seq = h + v
    else:
        seq = v + h
    return seq + "A"


def get_sequence(code, intermediate_keypads=2):
    """
    Return the sequence that I must type on a directional keypad,
    to instruct a robot typing on a directional keypad,
    to instruct a robot (bot1) typing on a directional keypad,
    to instruct a robot typing on a numeric keypad to type the given code (goal)
    """
    bot = "".join(directions(f, t, Keypad.NUMERIC) for f, t in zip("A" + code, code))
    for i in range(intermediate_keypads):
        bot = "".join(
            directions(f, t, Keypad.DIRECTIONS) for f, t in zip("A" + bot, bot)
        )
    return bot


def score(code, sequence):
    print(f"{len(sequence)} * {int(code[:-1])}")
    return len(sequence) * int(code[:-1])


def part1():
    codes = parse_input(read_input())
    sum = 0
    for code in codes:
        print(code)
        sequence = get_sequence(code)
        print(sequence)
        score_ = score(code, sequence)
        sum += score_
        print()
    return sum


def get_sequence_length(code, intermediate_keypads=2):
    @cache
    def recursive_directions(fr, to, keypads_left, first=True):
        if keypads_left == 0:
            return len(directions(fr, to, Keypad.DIRECTIONS))
        if first:
            bot_seq = directions(fr, to, Keypad.NUMERIC)
        else:
            bot_seq = directions(fr, to, Keypad.DIRECTIONS)
        return sum(
            recursive_directions(f, t, keypads_left - 1, first=False)
            for f, t in zip("A" + bot_seq, bot_seq)
        )

    result = 0
    for f, t in zip("A" + code, code):
        result += recursive_directions(f, t, intermediate_keypads)
    return result


def re_part1():
    codes = parse_input(read_input())
    return sum(int(code[:-1]) * get_sequence_length(code) for code in codes)


def part2():
    codes = parse_input(read_input())
    return sum(int(code[:-1]) * get_sequence_length(code, 25) for code in codes)


if __name__ == "__main__":
    print(part2())
