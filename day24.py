import sys


def read_input():
    with open(sys.argv[1]) as f:
        return f.read().strip()


def parse_input(data):
    valuesstr, connectionsstr = data.split("\n\n")
    values = {name: bool(int(value)) for name, value in (line.split(": ") for line in valuesstr.splitlines())}
    # ex: "x00 AND y00 -> z00"
    def from_line(line: str):
        in1, op, in2, _, out = line.split(" ")
        return in1, op, in2, out
    connections = { c for c in map(from_line, connectionsstr.splitlines())}
    for name1, _, name2, name3 in connections:
        for n in (name1, name2, name3):
            if n not in values:
                # Add a placeholder for unknown values.
                # I would just use a defaultdict or always .get,
                # but I want to use the keys as a definitive set of wire names.
                values[n] = None
    return values, connections

def eval_circuit(values, connections):
    new_connections = connections.copy()
    for name1, op, name2, output in connections:
        if values.get(output) is not None:
            # > There are no loops; once a gate has determined its output,
            # > the output will not change until the whole system is reset
            print(f"Skipping {name1} {op} {name2} -> {output}")
            continue
        if values.get(name1) is not None and values.get(name2) is not None:
            in1, in2 = values[name1], values[name2]
            o = None
            match op:
                case "AND":
                    o = in1 & in2
                case "OR":
                    o = in1 | in2
                case "XOR":
                    o = in1 ^ in2
                case _:
                    raise ValueError(f"Unknown operation {op}")
            values[output] = o
            # Popping the connection Keeps us from re-evaluating it, as does the check for output above
            new_connections.remove((name1, op, name2, output))
    return values, new_connections

def get_zs(values):
    return sorted({(name, value) for name, value in values.items() if name.startswith("z")}, key=lambda x: x[0])


def calc_z(zs):
    z_vals = map(lambda x: int(x[1]), reversed(zs))
    final_z = 0
    for z in z_vals:
        final_z <<= 1
        final_z |= z
    return final_z


def debug_print(values):
    for name in sorted(values.keys()):
        print(f"{name}: {int(values[name])}")


def part1():
    values, connections = parse_input(read_input())
    while any(z[1] is None for z in get_zs(values)):
        values, connections = eval_circuit(values, connections)
    return calc_z(get_zs(values))



if __name__ == "__main__":
    print(part1())
