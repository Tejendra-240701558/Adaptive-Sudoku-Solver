"""
Benchmark framework for the Adaptive Sudoku Solver.

This module runs the same Sudoku puzzles using multiple
solving strategies and records comparable performance data.
"""

import csv
import os
import time

from datasets.sudoku_benchmark import BENCHMARK_PUZZLES
from src.adaptive_solver import solve as adaptive_solve
from src.constraint_propagation import propagate
from src.min_conflicts import solve as min_conflicts_solve
from src.mrv_solver import solve as mrv_solve
from src.sudoku import Sudoku
from src.validator import is_valid


CONSTRAINT_PROPAGATION = "constraint_propagation"
MRV_BACKTRACKING = "mrv_backtracking"
MIN_CONFLICTS = "min_conflicts"
ADAPTIVE = "adaptive"


# Controlled Min-Conflicts budget for benchmarking.
MIN_CONFLICTS_MAX_STEPS = 5000
MIN_CONFLICTS_MAX_RESTARTS = 2


def run_min_conflicts(sudoku):
    """
    Run Min-Conflicts with a controlled benchmark budget.

    The production solver supports larger limits, but a bounded
    configuration prevents a single benchmark case from running
    indefinitely.
    """

    return min_conflicts_solve(
        sudoku,
        max_steps=MIN_CONFLICTS_MAX_STEPS,
        max_restarts=MIN_CONFLICTS_MAX_RESTARTS,
    )


STRATEGIES = {
    CONSTRAINT_PROPAGATION: propagate,
    MRV_BACKTRACKING: mrv_solve,
    MIN_CONFLICTS: run_min_conflicts,
    ADAPTIVE: adaptive_solve,
}


def run_solver(puzzle, solver):
    """
    Run one solver on a copy of the puzzle.

    Returns
    -------
    dict
        Benchmark results for the solver.
    """

    sudoku = Sudoku(puzzle)

    start_time = time.perf_counter()

    solved = solver(sudoku)

    end_time = time.perf_counter()

    elapsed_time = end_time - start_time

    return {
        "solved": solved,
        "valid_solution": solved and is_valid(sudoku),
        "solving_time": elapsed_time,
        "empty_cells_remaining": sudoku.empty_count(),
    }


def run_benchmark():
    """
    Run all configured strategies on all benchmark puzzles.
    """

    results = []

    for puzzle_name, puzzle in BENCHMARK_PUZZLES.items():

        print(f"\nRunning benchmark for {puzzle_name}...")

        for strategy_name, solver in STRATEGIES.items():

            print(
                f"  Running {strategy_name}...",
                end=" ",
                flush=True
            )

            result = run_solver(
                puzzle,
                solver
            )

            benchmark_result = {
                "puzzle": puzzle_name,
                "strategy": strategy_name,
                "solved": result["solved"],
                "valid_solution": result["valid_solution"],
                "solving_time": result["solving_time"],
                "empty_cells_remaining": result[
                    "empty_cells_remaining"
                ],
            }

            results.append(benchmark_result)

            print(
                f"done ({result['solving_time']:.6f}s)"
            )

    return results


def save_results(results, output_path):
    """
    Save benchmark results to a CSV file.
    """

    directory = os.path.dirname(output_path)

    if directory:
        os.makedirs(directory, exist_ok=True)

    fieldnames = [
        "puzzle",
        "strategy",
        "solved",
        "valid_solution",
        "solving_time",
        "empty_cells_remaining",
    ]

    with open(
        output_path,
        "w",
        newline="",
        encoding="utf-8"
    ) as csv_file:

        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(results)


if __name__ == "__main__":

    output_file = "benchmarks/benchmark_results.csv"

    benchmark_results = run_benchmark()

    save_results(
        benchmark_results,
        output_file
    )

    print()
    print("Benchmark completed.")
    print(f"Results saved to: {output_file}")

    print()
    print("Benchmark Summary:")

    for result in benchmark_results:
        print(
            f"{result['puzzle']} | "
            f"{result['strategy']} | "
            f"solved={result['solved']} | "
            f"valid={result['valid_solution']} | "
            f"time={result['solving_time']:.6f}s"
        )