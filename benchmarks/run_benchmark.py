"""
Run the complete Sudoku benchmark.

This script compares:
- Constraint Propagation
- MRV + Backtracking
- Min-Conflicts
- Adaptive Sudoku Solver

The results are saved to a CSV file for later analysis
and visualization.
"""

import csv
import time
from pathlib import Path

from datasets.generate_benchmark import generate_dataset
from src.adaptive_solver import solve as adaptive_solve
from src.constraint_propagation import propagate
from src.metrics import SolverMetrics
from src.min_conflicts import solve as min_conflicts_solve
from src.mrv_solver import solve as mrv_solve
from src.sudoku import Sudoku
from src.validator import is_valid


OUTPUT_FILE = Path(
    "benchmarks",
    "benchmark_results.csv",
)

MIN_CONFLICTS_MAX_STEPS = 1000
MIN_CONFLICTS_MAX_RESTARTS = 1


def run_solver(puzzle, solver_name):
    """
    Run one solver and collect performance metrics.

    Parameters
    ----------
    puzzle : list[list[int]]
        Sudoku puzzle.

    solver_name : str
        Name of the solver.

    Returns
    -------
    dict
        Benchmark result for the solver.
    """

    sudoku = Sudoku(puzzle)
    metrics = SolverMetrics()

    metrics.start_timer()

    if solver_name == "constraint_propagation":

        solved = propagate(
            sudoku,
            metrics=metrics,
        )

    elif solver_name == "mrv_backtracking":

        solved = mrv_solve(
            sudoku,
            metrics=metrics,
        )

    elif solver_name == "min_conflicts":

        solved = min_conflicts_solve(
            sudoku,
            max_steps=MIN_CONFLICTS_MAX_STEPS,
            max_restarts=MIN_CONFLICTS_MAX_RESTARTS,
            metrics=metrics,
        )

    elif solver_name == "adaptive":

        solved = adaptive_solve(
            sudoku,
            metrics=metrics,
        )

    else:
        raise ValueError(
            f"Unknown solver: {solver_name}"
        )

    metrics.stop_timer()

    valid_solution = (
        solved
        and sudoku.empty_count() == 0
        and is_valid(sudoku)
    )

    return {
        "solved": valid_solution,
        "solving_time": metrics.solving_time,
        "search_nodes": metrics.search_nodes,
        "backtracks": metrics.backtracks,
        "conflicts": metrics.conflicts,
        "cells_solved": metrics.cells_solved,
        "candidate_reductions": metrics.candidate_reductions,
        "strategy_switches": metrics.strategy_switches,
    }


def run_benchmark():
    """Run every solver on every benchmark puzzle."""

    dataset = generate_dataset()

    solver_names = [
        "constraint_propagation",
        "mrv_backtracking",
        "min_conflicts",
        "adaptive",
    ]

    results = []

    for puzzle_name, puzzle in dataset.items():

        print()
        print(f"Running {puzzle_name}...")

        for solver_name in solver_names:

            result = run_solver(
                puzzle,
                solver_name,
            )

            row = {
                "puzzle": puzzle_name,
                "empty_cells": sum(
                    row.count(0)
                    for row in puzzle
                ),
                "solver": solver_name,
                **result,
            }

            results.append(row)

            print(
                f"  {solver_name}: "
                f"solved={result['solved']} "
                f"time={result['solving_time']:.6f}s "
                f"nodes={result['search_nodes']} "
                f"backtracks={result['backtracks']} "
                f"conflicts={result['conflicts']} "
                f"switches={result['strategy_switches']}"
            )

    fieldnames = [
        "puzzle",
        "empty_cells",
        "solver",
        "solved",
        "solving_time",
        "search_nodes",
        "backtracks",
        "conflicts",
        "cells_solved",
        "candidate_reductions",
        "strategy_switches",
    ]

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with OUTPUT_FILE.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(results)

    print()
    print(
        f"Benchmark results saved to: "
        f"{OUTPUT_FILE}"
    )


if __name__ == "__main__":
    run_benchmark()