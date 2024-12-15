import sys


def read_input() -> str:
    with open(sys.argv[1]) as f:
        return f.read().strip()


def parse_data(data: str):
    (
        warehouse_str,
        movements_str,
    ) = data.split("\n\n")
    warehouse = {}
    for y, row in enumerate(warehouse_str.splitlines()):
        for x, cell in enumerate(row):
            warehouse[(x, y)] = cell
    movements = "".join(movements_str.splitlines())
    return warehouse, movements


def debug_print(wh, pos):
    maxx, maxy = max(k[0] for k in wh), max(k[1] for k in wh)
    for y in range(maxy + 1):
        for x in range(maxx + 1):
            if (x, y) == pos:
                print("@", end="")
            else:
                print(wh.get((x, y), " "), end="")
        print()


movements = {
    "^": (0, -1),
    ">": (1, 0),
    "v": (0, 1),
    "<": (-1, 0),
}


def move_box(wh, pos, direction):
    x, y = pos
    dx, dy = movements[direction]
    # We already know the next cell is a box.
    # Let's check cells from box to wall in direction and see if there's an empty space.
    while wh.get((x + dx, y + dy)) == "O":
        x += dx
        y += dy
    if wh.get((x + dx, y + dy)) == ".":
        # Move the front box to this empty space
        wh[(x + dx, y + dy)] = "O"
        # And move the player to the box's previous position
        new_pos = (pos[0] + dx, pos[1] + dy)
        wh[new_pos] = "."
        return wh, new_pos
    return wh, pos


def move(wh, pos, direction):
    x, y = pos
    dx, dy = movements[direction]
    if wh.get((x + dx, y + dy)) == "#":
        # Stop at walls
        return wh, pos
    if wh.get((x + dx, y + dy)) == "O":
        # It's a box, check if we can move it
        return move_box(wh, pos, direction)
    return wh, (x + dx, y + dy)


def gps_coordinates(box):
    return 100 * box[1] + box[0]


def part1():
    wh, movements = parse_data(read_input())
    pos = next(k for k, v in wh.items() if v == "@")
    wh[pos] = "."
    for dir in movements:
        wh, pos = move(wh, pos, dir)
    debug_print(wh, pos)
    return sum(gps_coordinates(k) if v == "O" else 0 for k, v in wh.items())


def doublewide_warehouse(wh):
    new_wh = {}
    for k, v in wh.items():
        match v:
            case "#":
                left, right = "#", "#"
            case ".":
                left, right = ".", "."
            case "O":
                left, right = "[", "]"
            case "@":
                left, right = "@", "."
        new_wh[(k[0] * 2, k[1])] = left
        new_wh[(k[0] * 2 + 1, k[1])] = right
    return new_wh


def move_stack(wh, accounted, pos, dir):
    new_wh = wh.copy()
    dx, dy = movements[dir]
    # First, clear them all out
    for p in accounted:
        new_wh[p] = "."
    # For each cell in acounted, move it in the direction dir.
    for p in accounted:
        # The new position of this cell
        new_p = (p[0] + dx, p[1] + dy)
        # Draw the new cell from the original cell
        new_wh[new_p] = wh[p]
    return new_wh, (pos[0] + dx, pos[1] + dy)


def move_wide_box(wh, pos, direction):
    x, y = pos
    dx, dy = movements[direction]
    # We already know the next cell is a box.
    # Let's check cells from box to wall in direction and see if there's an empty space.
    # For horizontal movement, we can still just move linearly.
    if dy == 0:
        accounted = set()
        while wh.get((x + dx, y)) in {"[", "]"}:
            x += dx
            accounted.add((x, y))
        if wh.get((x + dx, y)) == ".":
            # Move all of the boxes over 1 cell
            return move_stack(wh, accounted, pos, direction)
        return wh, pos
    # For vertical movement, through, we need to apply movement to both cells of the box.
    # We can't just move linearly.
    # First, find all of the leaf cells in the direction of movement.
    # These are the cells just beyond the boxes.
    # If any of them are walls, we can't move the boxes.
    # If all are empty, we can move all the boxes vertically one space.
    stack = []  # The next cells to check
    accounted = set()  # Box cells we've already checked
    stack.append((x + dx, y + dy))
    while stack:
        # Get the position we're checking
        p = stack.pop()
        cell = wh.get(p)
        # If we've seen it before, skip it
        if p in accounted:
            continue
        # If it's a wall, we can't move the boxes
        if cell == "#":
            return wh, pos
        # If it's empty space, continue without accounting for it - we don't want to "move" the empty space.
        if cell == ".":
            continue
        accounted.add(p)
        # If it's a box, add the other side to the stack
        if cell == "[":
            stack.append((p[0] + 1, p[1]))
        elif cell == "]":
            stack.append((p[0] - 1, p[1]))
        # And add the next cell in direction to the stack
        stack.append((p[0], p[1] + dy))
    else:
        # We've exhausted the stack without finding a wall, so we can move the boxes.
        return move_stack(wh, accounted, pos, direction)


def wide_move(wh, pos, direction):
    x, y = pos
    dx, dy = movements[direction]
    if wh.get((x + dx, y + dy)) == "#":
        return wh, pos
    if wh.get((x + dx, y + dy)) in {"[", "]"}:
        return move_wide_box(wh, pos, direction)
    return wh, (x + dx, y + dy)


def part2():
    wh, movements = parse_data(read_input())
    wh = doublewide_warehouse(wh)
    pos = next(k for k, v in wh.items() if v == "@")
    wh[pos] = "."
    for dir in movements:
        wh, pos = wide_move(wh, pos, dir)
    debug_print(wh, pos)
    return sum(gps_coordinates(k) if v == "[" else 0 for k, v in wh.items())


if __name__ == "__main__":
    print(part2())
