import sys
from typing import Generator

def parse_input() -> Generator[str, None,  None]:
    # Stream one line at a time from stdin
    for line in sys.stdin:
        yield line.strip()

def parse_report(line: str) -> list[int]:
    # Parse the level from the input
    return [int(x) for x in line.split()]

def rule1(report: list[int]) -> bool:
    # Check that the values are monotonically increasing OR decreasing
    return report == sorted(report) or report == sorted(report, reverse=True)

def rule2(report: list[int]) -> bool:
    # Check that the difference between adjacent values is between 1 and 3 inclusive
    return all(0 < abs(a - b) <= 3 for a, b in zip(report, report[1:]))

def is_safe(report: list[int]) -> bool:
    return rule1(report) and rule2(report)

def part1() -> int:
    # count the safe levels
    return sum(is_safe(parse_report(line)) for line in parse_input())

def generate_reports(report: list[int]) -> Generator[list[int], None, None]:
    yield report
    for i in range(len(report)):
        yield report[:i] + report[i+1:]

def is_safe2(report: list[int]) -> bool:
    # Same rules as before, but we can tolerate a single bad value.
    # Let's test that by simply removing a value until we have a safe report.
    return any(is_safe(r) for r in generate_reports(report))

def part2() -> int:
    # count the safe levels
    return sum(is_safe2(parse_report(line)) for line in parse_input())


if __name__ == "__main__":
    print(part2())
