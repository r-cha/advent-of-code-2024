import sys
from typing import NamedTuple


def read_input():
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            return f.read().strip()
    return sys.stdin.read().strip()


def parse_input(data) -> list[int]:
    block_id = 0
    blocks = []
    for i, char in enumerate(data):
        repeats = int(char)
        if i % 2 == 0:
            local_id = block_id
            block_id += 1
        else:
            local_id = -1
        for _ in range(repeats):
            blocks.append(local_id)
    return blocks


def compact(blocks: list[int]) -> list[int]:
    """Iteratively move the rightmost blocks to the leftmost empty spaces"""
    front, back = 0, len(blocks) - 1
    while front < back:
        # Move front to an empty block
        if blocks[front] != -1:
            front += 1
        # Move back to a non-empty block
        elif blocks[back] == -1:
            back -= 1
        # Move back to front
        if blocks[front] == -1 and blocks[back] != -1:
            blocks[front] = blocks[back]
            blocks[back] = -1
            front += 1
            back -= 1
    return blocks


def checksum(blocks: list[int]) -> int:
    return sum(i * block for i, block in enumerate(blocks) if block != -1)


def part1():
    data = read_input()
    blocks = parse_input(data)
    compacted = compact(blocks)
    return checksum(compacted)


class Runblock(NamedTuple):
    length: int
    block_id: int


def expand(runlength: list[Runblock]) -> list[int]:
    blocks = []
    for runblock in runlength:
        blocks.extend([runblock.block_id] * runblock.length)
    return blocks


def debug_print(blocks: list[int]):
    print("".join(str(block) if block != -1 else "." for block in blocks))


def debug_print_runblocks(blocks: list[Runblock]):
    debug_print(expand(blocks))


def parse_run_length(data: str) -> list[Runblock]:
    """Parse the run-length encoded data into tuples of run length and block id"""
    block_id = 0
    blocks = []
    for i in range(0, len(data), 2):
        data_length = int(data[i])
        try:
            skip_length = int(data[i + 1])
        except IndexError:
            skip_length = 0
        blocks.append(Runblock(data_length, block_id))
        blocks.append(Runblock(skip_length, -1))
        block_id += 1
    return blocks


def defrag(blocks: list[Runblock]) -> list[Runblock]:
    """
    Iteratively move the rightmost chunk of file to the leftmost free space

    > ... attempt to move whole files to the leftmost span of free space blocks that could fit the file.
    > Attempt to move each file exactly once in order of decreasing file ID number
    > starting with the file with the highest file ID number.
    > If there is no span of free space to the left of a file that is large enough to fit the file,
    > the file does not move.
    """
    back = len(blocks) - 1
    while back >= 0:
        front = 0
        backblock = blocks[back]
        if backblock.block_id == -1:
            # Skip free space
            back -= 1
            continue
        # Find empty space
        while front < back:
            frontblock = blocks[front]
            if frontblock.block_id != -1:
                # Skip data blocks
                front += 1
                continue
            if frontblock.length >= backblock.length:
                # Move the data block from the right to this empty space
                blocks[front] = backblock
                blocks[back] = Runblock(backblock.length, -1)
                new_front_skip_length = frontblock.length - backblock.length
                if new_front_skip_length > 0:
                    blocks.insert(front + 1, Runblock(new_front_skip_length, -1))
                    # This changes the indexing of the blocks, so DON'T decrement back
                else:
                    back -= 1
                break
            else:
                front += 1
        back -= 1
    return blocks


def part2():
    data = read_input()
    blocks = parse_run_length(data)
    compacted = defrag(blocks)
    expanded = expand(compacted)
    return checksum(expanded)


if __name__ == "__main__":
    print(part2())
