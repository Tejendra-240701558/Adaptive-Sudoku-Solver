"""
Generate a diverse Sudoku benchmark dataset.

The benchmark is created from several different valid completed
Sudoku grids. Sudoku-preserving row, column, band, stack, and
digit transformations are used to create structurally different
puzzle instances.

Each benchmark puzzle is created by removing a controlled number
of values from a known valid completed grid.
"""

import random


BASE_SOLUTION = [
    [5, 3, 4, 6, 7, 8, 9, 1, 2],
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 1, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 9],
]


def shuffle_solution(solution, seed):
    """
    Create a structurally different valid Sudoku solution.

    The transformation preserves Sudoku validity by using:
    - digit permutation
    - row permutations within bands
    - band permutations
    - column permutations within stacks
    - stack permutations
    """

    rng = random.Random(seed)

    grid = [
        row.copy()
        for row in solution
    ]

    # ---------------------------------------------------------
    # 1. Randomly rename the digits.
    # ---------------------------------------------------------

    digits = list(range(1, 10))
    shuffled_digits = digits.copy()
    rng.shuffle(shuffled_digits)

    digit_map = {
        original: shuffled
        for original, shuffled in zip(
            digits,
            shuffled_digits,
        )
    }

    grid = [
        [
            digit_map[value]
            for value in row
        ]
        for row in grid
    ]

    # ---------------------------------------------------------
    # 2. Shuffle rows within each 3-row band.
    # ---------------------------------------------------------

    bands = [
        grid[0:3],
        grid[3:6],
        grid[6:9],
    ]

    for band in bands:
        rng.shuffle(band)

    # ---------------------------------------------------------
    # 3. Shuffle the three row bands.
    # ---------------------------------------------------------

    rng.shuffle(bands)

    grid = [
        row
        for band in bands
        for row in band
    ]

    # ---------------------------------------------------------
    # 4. Shuffle columns within each 3-column stack.
    # ---------------------------------------------------------

    column_groups = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
    ]

    for group in column_groups:
        rng.shuffle(group)

    # ---------------------------------------------------------
    # 5. Shuffle the three column stacks.
    # ---------------------------------------------------------

    rng.shuffle(column_groups)

    columns = [
        column
        for group in column_groups
        for column in group
    ]

    grid = [
        [row[column] for column in columns]
        for row in grid
    ]

    return grid


def create_puzzle(solution, empty_cells, seed):
    """
    Create a Sudoku puzzle by removing a specified number
    of values from a completed solution.
    """

    rng = random.Random(seed)

    puzzle = [
        row.copy()
        for row in solution
    ]

    positions = [
        (row, col)
        for row in range(9)
        for col in range(9)
    ]

    removed = rng.sample(
        positions,
        empty_cells,
    )

    for row, col in removed:
        puzzle[row][col] = 0

    return puzzle


# Each tuple contains:
#
# (source solution seed, number of empty cells, removal seed)
#
# Different source seeds create different valid completed
# Sudoku structures.
BENCHMARK_CONFIG = {
    "puzzle_1": (101, 20, 1001),
    "puzzle_2": (202, 30, 2002),
    "puzzle_3": (303, 40, 3003),
    "puzzle_4": (404, 50, 4004),
    "puzzle_5": (505, 55, 5005),
    "puzzle_6": (606, 60, 6006),
    "puzzle_7": (707, 65, 7007),
    "puzzle_8": (808, 50, 8008),
}


def generate_dataset():
    """
    Generate the complete benchmark dataset.
    """

    dataset = {}

    for name, (
        solution_seed,
        empty_cells,
        removal_seed,
    ) in BENCHMARK_CONFIG.items():

        solution = shuffle_solution(
            BASE_SOLUTION,
            solution_seed,
        )

        puzzle = create_puzzle(
            solution,
            empty_cells,
            removal_seed,
        )

        dataset[name] = puzzle

    return dataset


def print_puzzle(name, puzzle):
    """Print one puzzle in Python-list format."""

    print(f'"{name}": [')

    for row in puzzle:
        print(f"    {row},")

    print("],")


if __name__ == "__main__":

    dataset = generate_dataset()

    for name, puzzle in dataset.items():
        print_puzzle(name, puzzle)