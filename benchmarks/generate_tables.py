"""
Generate numerical result tables from Sudoku benchmark results.

This module reads benchmark_results.csv and generates:

1. solver_summary.csv
2. detailed_results.csv

The generated tables are stored in results/tables/.
"""

import csv
from pathlib import Path


INPUT_FILE = Path(
    "benchmarks",
    "benchmark_results.csv",
)

OUTPUT_DIR = Path(
    "results",
    "tables",
)


SOLVERS = [
    "constraint_propagation",
    "mrv_backtracking",
    "min_conflicts",
    "adaptive",
]


SOLVER_LABELS = {
    "constraint_propagation": "Constraint Propagation",
    "mrv_backtracking": "MRV + Backtracking",
    "min_conflicts": "Min-Conflicts",
    "adaptive": "Adaptive",
}


def load_results():
    """Load benchmark results from the CSV file."""

    with INPUT_FILE.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as file:

        reader = csv.DictReader(file)

        return list(reader)


def create_output_directory():
    """Create the result table directory."""

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


def generate_solver_summary(results):
    """
    Generate the solver summary table.

    The summary contains:
    - solved puzzles
    - success percentage
    - average solving time
    - average search nodes
    - average backtracks
    - average strategy switches
    """

    output_file = OUTPUT_DIR / "solver_summary.csv"

    rows = []

    for solver in SOLVERS:

        solver_results = [
            row
            for row in results
            if row["solver"] == solver
        ]

        total_puzzles = len(solver_results)

        solved_count = sum(
            row["solved"].lower() == "true"
            for row in solver_results
        )

        success_rate = (
            solved_count / total_puzzles
        ) * 100

        average_time = (
            sum(
                float(row["solving_time"])
                for row in solver_results
            )
            / total_puzzles
        )

        average_nodes = (
            sum(
                int(row["search_nodes"])
                for row in solver_results
            )
            / total_puzzles
        )

        average_backtracks = (
            sum(
                int(row["backtracks"])
                for row in solver_results
            )
            / total_puzzles
        )

        average_switches = (
            sum(
                int(row["strategy_switches"])
                for row in solver_results
            )
            / total_puzzles
        )

        rows.append(
            {
                "solver": SOLVER_LABELS[solver],
                "solved": f"{solved_count}/{total_puzzles}",
                "success_rate_percent": f"{success_rate:.1f}",
                "average_solving_time_seconds": (
                    f"{average_time:.6f}"
                ),
                "average_search_nodes": (
                    f"{average_nodes:.2f}"
                ),
                "average_backtracks": (
                    f"{average_backtracks:.2f}"
                ),
                "average_strategy_switches": (
                    f"{average_switches:.2f}"
                ),
            }
        )

    fieldnames = [
        "solver",
        "solved",
        "success_rate_percent",
        "average_solving_time_seconds",
        "average_search_nodes",
        "average_backtracks",
        "average_strategy_switches",
    ]

    with output_file.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(rows)

    return output_file


def generate_detailed_results(results):
    """
    Generate a cleaned detailed-results table.

    One row represents one solver running on one puzzle.
    """

    output_file = OUTPUT_DIR / "detailed_results.csv"

    rows = []

    for row in results:

        rows.append(
            {
                "puzzle": row["puzzle"],
                "empty_cells": row["empty_cells"],
                "solver": SOLVER_LABELS[
                    row["solver"]
                ],
                "solved": row["solved"],
                "solving_time_seconds": (
                    row["solving_time"]
                ),
                "search_nodes": row["search_nodes"],
                "backtracks": row["backtracks"],
                "conflicts": row["conflicts"],
                "cells_solved": row["cells_solved"],
                "candidate_reductions": (
                    row["candidate_reductions"]
                ),
                "strategy_switches": (
                    row["strategy_switches"]
                ),
            }
        )

    fieldnames = [
        "puzzle",
        "empty_cells",
        "solver",
        "solved",
        "solving_time_seconds",
        "search_nodes",
        "backtracks",
        "conflicts",
        "cells_solved",
        "candidate_reductions",
        "strategy_switches",
    ]

    with output_file.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(rows)

    return output_file


def main():
    """Generate all result tables."""

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Benchmark file not found: {INPUT_FILE}"
        )

    create_output_directory()

    results = load_results()

    if not results:
        raise ValueError(
            "Benchmark results file is empty."
        )

    summary_file = generate_solver_summary(
        results
    )

    detailed_file = generate_detailed_results(
        results
    )

    print()
    print("Result tables generated successfully.")
    print()
    print(f"Summary table:  {summary_file}")
    print(f"Detailed table: {detailed_file}")


if __name__ == "__main__":
    main()