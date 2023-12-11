import pathlib
import sys
from collections import defaultdict
from itertools import combinations


def parse(parsedata):
    grid = defaultdict(str)
    emptyrows = set()
    emptycolumns = set()
    galaxies = set()

    for y, line in enumerate(parsedata.splitlines()):

        if line.count("#") == 0:
            emptyrows.add(y)

        for x, tile in enumerate(line):
            grid[x, y] = tile
            if tile == "#":
                galaxies.add((x, y))

    max_x = x
    max_y = y

    for x in range(0, max_x + 1):

        count = 0
        for y in range(0, max_y + 1):
            if grid[x, y] != ".":
                count += 1

        if count == 0:
            emptycolumns.add(x)

    return grid, galaxies, emptyrows, emptycolumns


def expanded_man_dist(a, b, emptyrows, emptycolumns, expansion):
    # off by one correction
    if expansion > 1:
        expansion = expansion - 1
    dist = abs(a[1] - b[1]) + abs(a[0] - b[0])
    passed_rows = set(range(*sorted((a[1], b[1]))))
    passed_cols = set(range(*sorted((a[0], b[0]))))
    for row in emptyrows:
        if row in passed_rows:
            dist += expansion
    for col in emptycolumns:
        if col in passed_cols:
            dist += expansion
    return dist


def part1(data):
    grid, galaxies, emptyrows, emptycolumns = data

    pathsum = 0
    for pairs in set(combinations(galaxies, 2)):
        pathsum += expanded_man_dist(pairs[0], pairs[1], emptyrows, emptycolumns, expansion=1)

    return pathsum


def part2(data):
    grid, galaxies, emptyrows, emptycolumns = data

    pathsum = 0
    for pairs in set(combinations(galaxies, 2)):
        pathsum += expanded_man_dist(pairs[0], pairs[1], emptyrows, emptycolumns, expansion=1_000_000)

    return pathsum


def solve(puzzle_data):
    data = parse(puzzle_data)
    solution1 = part1(data)
    solution2 = part2(data)
    return solution1, solution2


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"{path}:")
        puzzle_input = pathlib.Path(path).read_text().strip()
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))
