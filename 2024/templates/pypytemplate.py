import sys
from copy import deepcopy


def parse(parsedata):
    return ""

def part1(data):
    return ""

def part2(data):
    return ""

def solve(puzzle_data):
    data = parse(puzzle_data)
    solution1 = part1(deepcopy(data))
    solution2 = part2(data)
    return solution1, solution2


if __name__ == "__main__":
    for path in sys.argv[1:]:
        with open(path, 'r') as f:
            puzzle_input = f.read().strip()
        solutions = solve(puzzle_input)
        for solution in solutions:
            print(solution)