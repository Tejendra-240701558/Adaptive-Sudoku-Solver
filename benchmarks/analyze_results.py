"""
Analyze Sudoku benchmark results.

This script reads the benchmark CSV file and produces
summary statistics for each solving strategy.

It also saves the summary statistics to:
    results/performance_summary.csv
"""

import csv
from collections import defaultdict
from pathlib import Path


INPUT_FILE = Path(
    "benchmarks",
    "benchmark_results.csv",
)

OUTPUT_FILE = Path(
    "results",
    "performance_summary.csv",
)


def load_results():
    """Load benchmark results from the CSV file."""

    results = []

    with INPUT_FILE.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:
            row["empty_cells"] = int(row["empty_cells"])
            row["solved"] = row["solved"] == "True"
            row["solving_time"] = float(row["solving_time"])
            row["search_nodes"] = int(row["search_nodes"])
            row["backtracks"] = int(row["backtracks"])
            row["conflicts"] = int(row["conflicts"])
            row["cells_solved"] = int(row["cells_solved"])
            row["candidate_reductions"] = int(
                row["candidate_reductions"]
            )
            row["strategy_switches"] = int(
                row["strategy_switches"]
            )

            results.append(row)

    return results


def calculate_summary(results):
    """Calculate summary statistics for each solver."""

    grouped = defaultdict(list)

    for row in results:
        grouped[row["solver"]].append(row)

    summaries = []

    for solver, rows in grouped.items():

        solved_count = sum(
            row["solved"]
            for row in rows
        )

        total_count = len(rows)

        summaries.append(
            {
                "solver": solver,
                "puzzles": total_count,
                "solved": solved_count,
                "success_rate": (
                    solved_count / total_count * 100
                ),
                "average_time": (
                    sum(row["solving_time"] for row in rows)
                    / total_count
                ),
                "average_search_nodes": (
                    sum(row["search_nodes"] for row in rows)
                    / total_count
                ),
                "average_backtracks": (
                    sum(row["backtracks"] for row in rows)
                    / total_count
                ),
                "average_conflicts": (
                    sum(row["conflicts"] for row in rows)
                    / total_count
                ),
                "average_cells_solved": (
                    sum(row["cells_solved"] for row in rows)
                    / total_count
                ),
                "average_strategy_switches": (
                    sum(
                        row["strategy_switches"]
                        for row in rows
                    )
                    / total_count
                ),
            }
        )

    return summaries


def save_summary_csv(summaries):
    """Save solver summary statistics to a CSV file."""

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fieldnames = [
        "solver",
        "puzzles",
        "solved",
        "success_rate",
        "average_time",
        "average_search_nodes",
        "average_backtracks",
        "average_conflicts",
        "average_cells_solved",
        "average_strategy_switches",
    ]

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

        for summary in summaries:
            writer.writerow(
                {
                    "solver": summary["solver"],
                    "puzzles": summary["puzzles"],
                    "solved": summary["solved"],
                    "success_rate": (
                        f"{summary['success_rate']:.2f}"
                    ),
                    "average_time": (
                        f"{summary['average_time']:.6f}"
                    ),
                    "average_search_nodes": (
                        f"{summary['average_search_nodes']:.2f}"
                    ),
                    "average_backtracks": (
                        f"{summary['average_backtracks']:.2f}"
                    ),
                    "average_conflicts": (
                        f"{summary['average_conflicts']:.2f}"
                    ),
                    "average_cells_solved": (
                        f"{summary['average_cells_solved']:.2f}"
                    ),
                    "average_strategy_switches": (
                        f"{summary['average_strategy_switches']:.2f}"
                    ),
                }
            )

    print()
    print(
        f"Performance summary saved to: {OUTPUT_FILE}"
    )


def print_summary(summaries):
    """Print a formatted solver comparison table."""

    print()
    print("=" * 100)
    print("SOLVER SUMMARY")
    print("=" * 100)

    print(
        f"{'Solver':<25}"
        f"{'Solved':<10}"
        f"{'Success %':<12}"
        f"{'Avg Time':<14}"
        f"{'Avg Nodes':<14}"
        f"{'Avg Backtracks':<16}"
        f"{'Avg Switches':<14}"
    )

    print("-" * 100)

    for summary in summaries:

        print(
            f"{summary['solver']:<25}"
            f"{summary['solved']}/{summary['puzzles']:<7}"
            f"{summary['success_rate']:<12.1f}"
            f"{summary['average_time']:<14.6f}"
            f"{summary['average_search_nodes']:<14.2f}"
            f"{summary['average_backtracks']:<16.2f}"
            f"{summary['average_strategy_switches']:<14.2f}"
        )

    print("=" * 100)


def print_detailed_results(results):
    """Print benchmark results puzzle by puzzle."""

    print()
    print("=" * 100)
    print("DETAILED RESULTS")
    print("=" * 100)

    current_puzzle = None

    for row in results:

        if row["puzzle"] != current_puzzle:

            current_puzzle = row["puzzle"]

            print()
            print(
                f"{current_puzzle} "
                f"({row['empty_cells']} empty cells)"
            )

            print("-" * 80)

        print(
            f"  {row['solver']:<25}"
            f"time={row['solving_time']:.6f}s  "
            f"solved={row['solved']}  "
            f"nodes={row['search_nodes']}  "
            f"backtracks={row['backtracks']}  "
            f"conflicts={row['conflicts']}  "
            f"switches={row['strategy_switches']}"
        )


def main():
    """Run benchmark analysis."""

    if not INPUT_FILE.exists():
        print(
            f"Benchmark file not found: {INPUT_FILE}"
        )
        return

    results = load_results()

    summaries = calculate_summary(results)

    print_summary(summaries)
    print_detailed_results(results)
    save_summary_csv(summaries)


if __name__ == "__main__":
    main()