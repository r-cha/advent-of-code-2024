import sys


def read_input():
    with open(sys.argv[1]) as f:
        return f.read().strip()


def parse_input(data):
    valuesstr, connectionsstr = data.split("\n\n")
    values = {
        name: bool(int(value))
        for name, value in (line.split(": ") for line in valuesstr.splitlines())
    }

    # ex: "x00 AND y00 -> z00"
    def from_line(line: str):
        in1, op, in2, _, out = line.split(" ")
        return in1, op, in2, out

    connections = {c for c in map(from_line, connectionsstr.splitlines())}
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
            # Popping the connection keeps us from re-evaluating it, as does the check for output above
            new_connections.remove((name1, op, name2, output))
    return values, new_connections


def get_number_wires(values, title):
    # This gets the wires with agiven prefix
    # (x and y are used for inputs, and z for out)
    # then sorts them by name.
    # Their significance is determined by their name, e.g. z00 is the least significant bit.
    return sorted(
        {(name, value) for name, value in values.items() if name.startswith(title)},
        key=lambda x: x[0],
    )


def get_zs(values):
    return get_number_wires(values, "z")


def calc_from_bits(zs):
    # The bits are always named from least significant to most significant,
    # And they are sorted by significance when passed in here.
    z_vals = map(lambda x: int(x[1]), reversed(zs))
    final_z = 0
    for z in z_vals:
        final_z <<= 1
        final_z |= z
    return final_z


def simulate(values, connections):
    while any(z[1] is None for z in get_zs(values)):
        prev_values = values.copy()
        values, connections = eval_circuit(values, connections)
        if prev_values == values:
            return 0
    return calc_from_bits(get_zs(values))


def part1():
    values, connections = parse_input(read_input())
    return simulate(values, connections)


# Part 2, the great beast.
# Solution inspired by https://x.com/relizarov/status/1871547973072826821


def evaluate_gate(op, in1, in2):
    # operations will ONLY EVER be AND, OR, or XOR
    match op:
        case "AND":
            return in1 & in2
        case "OR":
            return in1 | in2
        case "XOR":
            return in1 ^ in2
        case _:
            raise ValueError(f"Unknown operation {op}")


def simulate_connection(values, connection):
    """Simulate a single connection if its inputs are known"""
    name1, op, name2, _ = connection
    if values.get(name1) is not None and values.get(name2) is not None:
        in1, in2 = values[name1], values[name2]
        return evaluate_gate(op, in1, in2)
    return None


def propagate_values(values, connections):
    """Propagate values through the network until no changes occur"""
    values = values.copy()
    max_iterations = len(connections) ** 2
    iterations = 0
    while iterations < max_iterations:
        prev_values = values.copy()
        for connection in connections:
            output = connection[3]
            if values.get(output) is None:
                o = simulate_connection(values, connection)
                if o is not None:
                    values[output] = o
        if prev_values == values:
            break
        iterations += 1
    return values


def swap_outputs(connections, swapped_pairs):
    new_connections = set()
    for connection in connections:
        for out1, out2 in swapped_pairs:
            if connection[3] == out1:
                new_connections.add((connection[0], connection[1], connection[2], out2))
            elif connection[3] == out2:
                new_connections.add((connection[0], connection[1], connection[2], out1))
            else:
                new_connections.add(connection)
    return new_connections


def validate_bit_position(connections, swapped_pairs, bit_position, carry):
    """Validates if current swapped configuration works for this bit position"""
    print(f"Validating bit position {bit_position}, {len(swapped_pairs)} swaps")
    # First, get relevant io for this bit position
    x_name, y_name, z_name = [f"{name}{bit_position:02d}" for name in "xyz"]

    # Try all possible input combinations
    for x, y in ((0, 0), (0, 1), (1, 0), (1, 1)):
        state = {x_name: bool(x), y_name: bool(y)}

        # Swap outputs BEFORE propagating values
        connections = swap_outputs(connections, swapped_pairs)

        final_state = propagate_values(state, connections)

        # Calculate the expected result
        bit_sum = x + y + int(carry)
        expected_z = bool(bit_sum & 1)
        new_carry = bool(bit_sum > 1)

        # Verify result
        if final_state.get(z_name) != expected_z:
            return None

        carry = new_carry

    return carry


def try_swaps(connections, bit_position, current_swaps, used_outputs):
    """Recursively try different output swaps until finding a valid configuration"""
    # Base case: we have 4 pairs of swaps already
    if len(current_swaps) == 4:
        carry = False
        for pos in range(bit_position + 1):
            carry = validate_bit_position(connections, current_swaps, pos, carry)
            if carry is None:
                return None
        return current_swaps

    # Recursive case: try swapping outputs
    outputs = {connection[3] for connection in connections}
    available = list(outputs - used_outputs)

    for i, out1 in enumerate(available):
        for out2 in available[i + 1 :]:
            new_swaps = current_swaps + [(out1, out2)]
            new_used = used_outputs | {out1, out2}
            carry_out = validate_bit_position(connections, new_swaps, bit_position, False)
            if carry_out is not None:
                next_result = try_swaps(connections, bit_position+1, new_swaps, new_used)
                if next_result is not None:
                    return next_result

    return None


def solve_circuit(values, connections):
    """Solve this circuit by finding the 4 pairs of swapped outputs"""
    result = try_swaps(connections, 0, [], set())

    if result is None:
        raise ValueError("No valid configuration found")

    return result


def part2():
    values, connections = parse_input(read_input())
    swaps = solve_circuit(values, connections)
    flattened = [item for sublist in swaps for item in sublist]
    return ",".join(name for name in sorted(flattened))


if __name__ == "__main__":
    print(part2())
