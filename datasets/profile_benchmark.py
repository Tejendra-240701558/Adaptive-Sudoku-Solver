"""
Profile candidate Sudoku benchmark puzzles.

This script compares the three individual solving strategies
on the generated candidate dataset.
"""

import time

from datasets.generate_benchmark import generate_dataset
from src.constraint_propagation import propagate
from src.min_conflicts import solve as min_conflicts_solve
from src.mrv_solver import solve as mrv_solve
from src.sudoku import Sudoku


MIN_CONFLICTS_MAX_STEPS = 1000
MIN_CONFLICTS_MAX_RESTARTS = 1


def measure(puzzle, solver):
    """Measure the execution time of one solver."""

    sudoku = Sudoku(puzzle)

    start = time.perf_counter()

    solved = solver(sudoku)

    elapsed = time.perf_counter() - start

    return solved, elapsed, sudoku.empty_count()


def run_min_conflicts(sudoku):
    """Run Min-Conflicts with a bounded profiling budget."""

    return min_conflicts_solve(
        sudoku,
        max_steps=MIN_CONFLICTS_MAX_STEPS,
        max_restarts=MIN_CONFLICTS_MAX_RESTARTS,
    )


def profile_dataset():
    """Profile all generated benchmark candidates."""

    dataset = generate_dataset()

    for name, puzzle in dataset.items():

        cp_solved, cp_time, cp_empty = measure(
            puzzle,
            propagate,
        )

        mrv_solved, mrv_time, mrv_empty = measure(
            puzzle,
            mrv_solve,
        )

        mc_solved, mc_time, mc_empty = measure(
            puzzle,
            run_min_conflicts,
        )

        print(
            f"{name}: "
            f"CP={cp_time:.6f}s "
            f"(solved={cp_solved}, empty={cp_empty}) | "
            f"MRV={mrv_time:.6f}s "
            f"(solved={mrv_solved}, empty={mrv_empty}) | "
            f"MC={mc_time:.6f}s "
            f"(solved={mc_solved}, empty={mc_empty})"
        )


if __name__ == "__main__":
    profile_dataset()