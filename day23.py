import sys
from collections import defaultdict


def read_input():
    with open(sys.argv[1]) as f:
        return f.read().strip()


def parse_input(data):
    """Return an edge map from the list of edges."""
    edges = defaultdict(set)
    for line in data.splitlines():
        a, b = line.split("-")
        edges[a].add(b)
        edges[b].add(a)
    return edges


def sets_of_three(edges):
    """Find cycles of length 3 in the graph"""
    threes = set()
    rem_nodes = set(edges.keys())
    while rem_nodes:
        a = rem_nodes.pop()
        for b in edges[a] & rem_nodes:
            for c in edges[b] & rem_nodes & edges[a]:
                threes.add(tuple(sorted([a, b, c])))
    return threes


def filter_for_ts(threes):
    return [s for s in threes if any(x.startswith("t") for x in s)]


def part1():
    edges = parse_input(read_input())
    threes = sets_of_three(edges)
    return len(filter_for_ts(threes))


def maximum_clique(edges):
    def bk(r, p, x):
        nonlocal max_clique
        if not p and not x:
            if len(r) > len(max_clique):
                max_clique = r.copy()
            return
        u = max(p | x, key=lambda v: len(edges[v] & p))
        for v in p - edges[u]:
            new_r = r | {v}
            new_p = p & edges[v]
            new_x = x & edges[v]
            bk(new_r, new_p, new_x)
            p.remove(v)
            x.add(v)
        return

    max_clique = set()
    bk(set(), set(edges.keys()), set())
    return max_clique


def part2():
    edges = parse_input(read_input())
    max_clique = maximum_clique(edges)
    return ",".join(sorted(list(max_clique)))


if __name__ == "__main__":
    print(part2())
