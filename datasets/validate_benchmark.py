"""
Validate the generated Sudoku benchmark dataset.

This script checks that every benchmark puzzle has:
- a valid Sudoku structure
- valid cell values
- no duplicate clues
- at least one solution using MRV backtracking
"""

from datasets.generate_benchmark import generate_dataset
from src.mrv_solver import solve
from src.sudoku import Sudoku
from src.validator import is_valid


def validate_dataset():
    """Validate every generated benchmark puzzle."""

    dataset = generate_dataset()

    all_valid = True

    for name, puzzle in dataset.items():

        sudoku = Sudoku(puzzle)

        valid_input = is_valid(sudoku)

        solved = False

        if valid_input:
            solved = solve(sudoku)

        print(
            f"{name}: "
            f"valid_input={valid_input}, "
            f"solvable={solved}, "
            f"empty={sum(row.count(0) for row in puzzle)}"
        )

        if not valid_input or not solved:
            all_valid = False

    print()

    if all_valid:
        print("All benchmark puzzles are valid and solvable.")
    else:
        print("One or more benchmark puzzles failed validation.")


if __name__ == "__main__":
    validate_dataset()