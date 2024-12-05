from collections import namedtuple
import sys


def read_input():
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            return f.read().strip()
    return sys.stdin.read().strip()


Rule = namedtuple("Rule", ["before", "after"])
Update = list[int]


def parse_input(data: str) -> tuple[list[Rule], list[Update]]:
    rulestr, updatestr = data.split("\n\n")
    rules = [
        (int(before), int(after))
        for before, after in (line.split("|") for line in rulestr.split("\n"))
    ]
    updates = [[int(x) for x in line.split(",")] for line in updatestr.split("\n")]

    return rules, updates


def satisfies_rule(update: Update, rule: Rule) -> bool:
    before, after = rule
    if not (before in update and after in update):
        # Rules only apply if both pages are present
        return True
    bi = update.index(before)
    ai = update.index(after)
    return bi < ai


def middle_value(update: Update) -> int:
    return update[len(update) // 2]


def part1() -> int:
    """Sum the middle value of each update that satisfies all the rules"""
    rules, updates = parse_input(read_input())
    return sum(
        middle_value(update)
        for update in updates
        if all(satisfies_rule(update, rule) for rule in rules)
    )


def correct_update(update: Update, rules: list[Rule]) -> Update:
    """Correct an update to satisfy all the rules"""
    while not all(satisfies_rule(update, rule) for rule in rules):
        for rule in rules:
            if not satisfies_rule(update, rule):
                before, after = rule
                bi = update.index(before)
                ai = update.index(after)
                if bi > ai:
                    update[bi], update[ai] = update[ai], update[bi]
    return update


def part2() -> int:
    """Correct incorrect updates and add *their* middle values"""
    rules, updates = parse_input(read_input())

    incorrect_updates = [
        update
        for update in updates
        if not all(satisfies_rule(update, rule) for rule in rules)
    ]
    for update in incorrect_updates:
        correct_update(update, rules)
    return sum(middle_value(update) for update in incorrect_updates)


if __name__ == "__main__":
    print(part2())
