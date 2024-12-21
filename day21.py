import sys
from functools import cache


def read_input():
    with open(sys.argv[1]) as f:
        return f.read().strip()

def parse_input(data):
    return data.splitlines()

directional_keypad = {
                 "^": (1, 0), "A": (2, 0),
    "<": (0, 1), "v": (1, 1), ">": (2, 1),
}

numeric_keypad = {
    "7": (0, 0), "8": (1, 0), "9": (2, 0),
    "4": (0, 1), "5": (1, 1), "6": (2, 1),
    "1": (0, 2), "2": (1, 2), "3": (2, 2),
                 "0": (1, 3), "A": (2, 3),
}


@cache
def _directions(fr, to, avoid=(0,0)):
    """
    Give the sequence of directions to go from one point to another.
    NOTE: We must always avoid the empty spaces in the keypads:
          (0,0) in the directional keypad and (0,3) in the numeric.
          So we'll use the param `avoid` to ensure we go the safest route.
    """
    from_x, from_y = fr
    to_x, to_y = to
    dx = to_x - from_x
    dy = to_y - from_y
    seq = ""
    if avoid == (0,0):
        # This is the directional keypad, avoid (0,0)
        if dy < 0: # Going up
            # Go horizontal first
            seq += ">" * dx if dx > 0 else "<" * abs(dx)
            seq += "^" * abs(dy)
        else: # Going down
            # Go vertical first
            seq += "v" * dy
            seq += ">" * dx if dx > 0 else "<" * abs(dx)
    else:
        # This is the numeric keypad; the problem is at (0,3)
        if dx < 0: # Going left
            # Go vertical first
            seq += "^" * abs(dy) if dy < 0 else "v" * dy
            seq += "<" * abs(dx)
        else: # Going right
            # Go horizontal first
            seq += ">" * dx
            seq += "^" * abs(dy) if dy < 0 else "v" * dy
    return seq + "A"


def get_sequence(code, intermediate_keypads=2):
    """
    Return the sequence that I must type on a directional keypad,
    to instruct a robot typing on a directional keypad, 
    to instruct a robot (bot1) typing on a directional keypad,
    to instruct a robot typing on a numeric keypad to type the given code (goal)
    """
    bot = "".join(_directions(numeric_keypad[f], numeric_keypad[t], (0,3)) for f, t in zip("A" + code, code))
    for i in range(intermediate_keypads):
        print(bot)
        bot = "".join(_directions(directional_keypad[f], directional_keypad[t]) for f, t in zip("A" + bot, bot))
    return bot

def score(code, sequence):
    print(f"{len(sequence)} * {int(code[:-1])}")
    return len(sequence) * int(code[:-1])


# 187118 too high


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

if __name__ == "__main__":
    print(part1())
