"""
Run the complete Sudoku benchmark.

This script compares:
- Constraint Propagation
- MRV + Backtracking
- Min-Conflicts
- Adaptive Sudoku Solver

The benchmark results are saved to a CSV file and can also
be reused by the main presentation program for overall analysis.
"""

import csv
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


SOLVER_NAMES = [
    "constraint_propagation",
    "mrv_backtracking",
    "min_conflicts",
    "adaptive",
]


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


def run_benchmark(verbose=True):
    """
    Run every solver on every benchmark puzzle.

    Parameters
    ----------
    verbose : bool
        If True, print individual benchmark results.

    Returns
    -------
    list[dict]
        Complete benchmark results.
    """

    dataset = generate_dataset()

    results = []

    for puzzle_name, puzzle in dataset.items():

        if verbose:
            print()
            print(f"Running {puzzle_name}...")

        for solver_name in SOLVER_NAMES:

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

            if verbose:
                print(
                    f"  {solver_name}: "
                    f"solved={result['solved']} "
                    f"time={result['solving_time']:.6f}s "
                    f"nodes={result['search_nodes']} "
                    f"backtracks={result['backtracks']} "
                    f"conflicts={result['conflicts']} "
                    f"switches={result['strategy_switches']}"
                )

    save_results(results)

    return results


def save_results(results):
    """
    Save benchmark results to the CSV file.

    Parameters
    ----------
    results : list[dict]
        Benchmark results.
    """

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


def calculate_summary(results):
    """
    Calculate overall performance statistics for each solver.

    Parameters
    ----------
    results : list[dict]
        Complete benchmark results.

    Returns
    -------
    dict
        Summary statistics grouped by solver.
    """

    summary = {}

    for solver_name in SOLVER_NAMES:

        solver_results = [
            result
            for result in results
            if result["solver"] == solver_name
        ]

        total_puzzles = len(solver_results)

        solved_puzzles = sum(
            1
            for result in solver_results
            if result["solved"]
        )

        success_rate = (
            solved_puzzles / total_puzzles * 100
            if total_puzzles
            else 0.0
        )

        average_time = (
            sum(
                result["solving_time"]
                for result in solver_results
            )
            / total_puzzles
            if total_puzzles
            else 0.0
        )

        average_nodes = (
            sum(
                result["search_nodes"]
                for result in solver_results
            )
            / total_puzzles
            if total_puzzles
            else 0.0
        )

        average_backtracks = (
            sum(
                result["backtracks"]
                for result in solver_results
            )
            / total_puzzles
            if total_puzzles
            else 0.0
        )

        average_conflicts = (
            sum(
                result["conflicts"]
                for result in solver_results
            )
            / total_puzzles
            if total_puzzles
            else 0.0
        )

        average_switches = (
            sum(
                result["strategy_switches"]
                for result in solver_results
            )
            / total_puzzles
            if total_puzzles
            else 0.0
        )

        summary[solver_name] = {
            "solved": solved_puzzles,
            "total": total_puzzles,
            "success_rate": success_rate,
            "average_time": average_time,
            "average_nodes": average_nodes,
            "average_backtracks": average_backtracks,
            "average_conflicts": average_conflicts,
            "average_switches": average_switches,
        }

    return summary


def get_adaptive_analysis(results):
    """
    Extract the adaptive solver's strategy sequence
    for every benchmark puzzle.

    Parameters
    ----------
    results : list[dict]
        Complete benchmark results.

    Returns
    -------
    list[dict]
        Adaptive strategy information for each puzzle.
    """

    adaptive_results = [
        result
        for result in results
        if result["solver"] == "adaptive"
    ]

    analysis = []

    for result in adaptive_results:

        analysis.append(
            {
                "puzzle": result["puzzle"],
                "empty_cells": result["empty_cells"],
                "switches": result["strategy_switches"],
            }
        )

    return analysis


def run_benchmark_analysis():
    """
    Run the complete benchmark and display an overall analysis.

    This function is intended for use by main.py.
    """

    print()
    print("=" * 72)
    print("                 COMPLETE BENCHMARK ANALYSIS")
    print("=" * 72)

    print()
    print("Running benchmark on all 8 Sudoku puzzles...")
    print()

    results = run_benchmark(verbose=False)

    summary = calculate_summary(results)

    print()
    print("-" * 72)
    print("SOLVER SUMMARY")
    print("-" * 72)

    print(
        f"{'Solver':<28}"
        f"{'Solved':<12}"
        f"{'Success':<12}"
        f"{'Avg Time':<15}"
    )

    print("-" * 72)

    display_names = {
        "constraint_propagation": "Constraint Propagation",
        "mrv_backtracking": "MRV + Backtracking",
        "min_conflicts": "Min-Conflicts",
        "adaptive": "Adaptive",
    }

    for solver_name in SOLVER_NAMES:

        data = summary[solver_name]

        solved_text = (
            f"{data['solved']}/{data['total']}"
        )

        success_text = (
            f"{data['success_rate']:.1f}%"
        )

        time_text = (
            f"{data['average_time']:.6f} s"
        )

        print(
            f"{display_names[solver_name]:<28}"
            f"{solved_text:<12}"
            f"{success_text:<12}"
            f"{time_text:<15}"
        )

    print()
    print("-" * 72)
    print("DETAILED PERFORMANCE SUMMARY")
    print("-" * 72)

    print(
        f"{'Solver':<28}"
        f"{'Nodes':<12}"
        f"{'Backtracks':<14}"
        f"{'Conflicts':<14}"
        f"{'Switches':<10}"
    )

    print("-" * 72)

    for solver_name in SOLVER_NAMES:

        data = summary[solver_name]

        print(
            f"{display_names[solver_name]:<28}"
            f"{data['average_nodes']:<12.2f}"
            f"{data['average_backtracks']:<14.2f}"
            f"{data['average_conflicts']:<14.2f}"
            f"{data['average_switches']:<10.2f}"
        )

    print()
    print("-" * 72)
    print("ADAPTIVE STRATEGY ANALYSIS")
    print("-" * 72)

    adaptive_analysis = get_adaptive_analysis(results)

    for item in adaptive_analysis:

        puzzle = item["puzzle"]
        empty_cells = item["empty_cells"]
        switches = item["switches"]

        print(
            f"{puzzle:<12}"
            f"Empty cells: {empty_cells:<5}"
            f"Switches: {switches}"
        )

    print()
    print("-" * 72)
    print(
        f"Benchmark results saved to: {OUTPUT_FILE}"
    )
    print("-" * 72)

    print()
    print("Benchmark analysis completed.")
    print()


if __name__ == "__main__":
    run_benchmark()