import re
import sys


def read_input():
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            return f.read().strip()
    return sys.stdin.read().strip()


def rotate_90_degrees(data: list[str]) -> list[str]:
    new_data = []
    for i in range(len(data[0])):
        new_row = ""
        for j in range(len(data)):
            new_row += data[len(data) - 1 - j][i]
        new_data.append(new_row)
    return new_data


def rotate_45_degrees(data: list[str]) -> list[str]:
    # rotate the matrix 45 degrees, e.g.
    #              C
    # > A B C      B F
    # > D E F  ->  A E I
    # > G H I      D H
    #              G
    new_data = []
    max_index_sum = len(data) + len(data[0]) - 1

    for s in range(max_index_sum):
        new_row = ""
        for i in range(max(len(data), len(data[0]))):
            j = s - i
            if 0 <= i < len(data) and 0 <= j < len(data[0]):
                new_row += data[i][j]
        if new_row:
            new_data.append(new_row)

    return new_data


def count_xmas(data: str) -> int:
    ninety_deg = "\n".join(rotate_90_degrees(data.split("\n")))
    forty_five = "\n".join(rotate_45_degrees(data.split("\n")))
    forty_five_rev = "\n".join(rotate_45_degrees(ninety_deg.split("\n")))

    match_expression = r"XMAS"

    foreward = re.findall(match_expression, data)
    backward = re.findall(match_expression, data[::-1])
    up = re.findall(match_expression, ninety_deg)
    down = re.findall(match_expression, ninety_deg[::-1])
    diag = re.findall(match_expression, forty_five)
    diag_rev = re.findall(match_expression, forty_five[::-1])
    other_diag = re.findall(match_expression, forty_five_rev)
    other_diag_rev = re.findall(match_expression, forty_five_rev[::-1])

    return (
        len(foreward)
        + len(backward)
        + len(up)
        + len(down)
        + len(diag)
        + len(diag_rev)
        + len(other_diag)
        + len(other_diag_rev)
    )


def arr_get(data: list[str], i: int, j: int) -> str:
    if 0 <= i < len(data) and 0 <= j < len(data[0]):
        return data[i][j]
    return None


def count_x_mas(data: str) -> int:
    arr = data.split("\n")

    total = 0
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            if arr[i][j] == "A":
                if (
                    (
                        arr_get(arr, i - 1, j - 1) == "M"
                        and arr_get(arr, i + 1, j + 1) == "S"
                    )
                    or (
                        arr_get(arr, i - 1, j - 1) == "S"
                        and arr_get(arr, i + 1, j + 1) == "M"
                    )
                ) and (
                    (
                        arr_get(arr, i - 1, j + 1) == "M"
                        and arr_get(arr, i + 1, j - 1) == "S"
                    )
                    or (
                        arr_get(arr, i - 1, j + 1) == "S"
                        and arr_get(arr, i + 1, j - 1) == "M"
                    )
                ):
                    total += 1

    return total


def part1() -> int:
    data = read_input()
    return count_xmas(data)


def part2() -> int:
    data = read_input()
    return count_x_mas(data)


if __name__ == "__main__":
    print(part2())
