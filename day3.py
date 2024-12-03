import re
import sys


def read_input() -> str:
    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as f:
            return f.read()
    return sys.stdin.read()


def part1() -> int:
    data = read_input()
    value_pairs = re.findall(r'mul\((\d+),(\d+)\)', data)
    return sum(int(a) * int(b) for a, b in value_pairs)

def part2() -> int:
    data = read_input()
    total = 0
    do_data = data.split('do()')
    for do in do_data:
        dont_data = do.split("don't()")
        use_this_data = dont_data[0]
        value_pairs = re.findall(r'mul\((\d+),(\d+)\)', use_this_data)
        total += sum(int(a) * int(b) for a, b in value_pairs)
    return total


if __name__ == '__main__':
    print(part2())
