"""
Profile the adaptive Sudoku solver on benchmark candidates.

This script evaluates how the adaptive solver behaves on
different Sudoku puzzle characteristics.
"""

import time

from datasets.generate_benchmark import generate_dataset
from src.adaptive_solver import solve as adaptive_solve
from src.sudoku import Sudoku


def measure(puzzle):
    """Measure the adaptive solver on one Sudoku puzzle."""

    sudoku = Sudoku(puzzle)

    start = time.perf_counter()

    solved = adaptive_solve(sudoku)

    elapsed = time.perf_counter() - start

    return solved, elapsed, sudoku.empty_count()


def profile_dataset():
    """Profile all generated benchmark candidates."""

    dataset = generate_dataset()

    for name, puzzle in dataset.items():

        solved, elapsed, empty = measure(puzzle)

        print(
            f"{name}: "
            f"time={elapsed:.6f}s "
            f"(solved={solved}, empty={empty})"
        )


if __name__ == "__main__":
    profile_dataset()