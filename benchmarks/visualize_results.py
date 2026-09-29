"""
Visualize Sudoku benchmark results.

This module reads benchmark_results.csv and generates
report-ready graphs for the Adaptive Sudoku Solver project.

Generated figures:
1. Average solving time
2. Solver success rate
3. Average search nodes
4. Adaptive strategy switches per puzzle
5. Empty cells vs solving time
"""

import csv
from pathlib import Path

import matplotlib.pyplot as plt


INPUT_FILE = Path(
    "benchmarks",
    "benchmark_results.csv",
)

OUTPUT_DIR = Path(
    "results",
    "graphs",
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
    """Create the graph output directory if necessary."""

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


def plot_average_solving_time(results):
    """Generate average solving time comparison."""

    labels = [
        "Constraint\nPropagation",
        "MRV +\nBacktracking",
        "Min-Conflicts",
        "Adaptive",
    ]

    averages = []

    for solver in SOLVERS:

        times = [
            float(row["solving_time"])
            for row in results
            if row["solver"] == solver
        ]

        averages.append(
            sum(times) / len(times)
        )

    plt.figure(figsize=(9, 6))

    bars = plt.bar(
        labels,
        averages,
    )

    plt.title(
        "Average Solving Time by Solver",
        fontsize=14,
        fontweight="bold",
    )

    plt.xlabel("Solver")
    plt.ylabel("Average Time (seconds)")

    plt.grid(
        axis="y",
        linestyle="--",
        alpha=0.4,
    )

    for bar, value in zip(
        bars,
        averages,
    ):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{value:.6f}",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "average_solving_time.png",
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()


def plot_success_rate(results):
    """Generate solver success-rate comparison."""

    labels = [
        "Constraint\nPropagation",
        "MRV +\nBacktracking",
        "Min-Conflicts",
        "Adaptive",
    ]

    success_rates = []

    for solver in SOLVERS:

        solver_results = [
            row
            for row in results
            if row["solver"] == solver
        ]

        solved_count = sum(
            row["solved"].lower() == "true"
            for row in solver_results
        )

        success_rate = (
            solved_count / len(solver_results)
        ) * 100

        success_rates.append(success_rate)

    plt.figure(figsize=(9, 6))

    bars = plt.bar(
        labels,
        success_rates,
    )

    plt.title(
        "Solver Success Rate",
        fontsize=14,
        fontweight="bold",
    )

    plt.xlabel("Solver")
    plt.ylabel("Success Rate (%)")

    plt.ylim(
        0,
        110,
    )

    plt.grid(
        axis="y",
        linestyle="--",
        alpha=0.4,
    )

    for bar, value in zip(
        bars,
        success_rates,
    ):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 2,
            f"{value:.1f}%",
            ha="center",
            va="bottom",
            fontsize=10,
        )

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "success_rate.png",
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()


def plot_average_search_nodes(results):
    """Generate average search-node comparison."""

    labels = [
        "Constraint\nPropagation",
        "MRV +\nBacktracking",
        "Min-Conflicts",
        "Adaptive",
    ]

    averages = []

    for solver in SOLVERS:

        nodes = [
            int(row["search_nodes"])
            for row in results
            if row["solver"] == solver
        ]

        averages.append(
            sum(nodes) / len(nodes)
        )

    plt.figure(figsize=(9, 6))

    bars = plt.bar(
        labels,
        averages,
    )

    plt.title(
        "Average Search Nodes by Solver",
        fontsize=14,
        fontweight="bold",
    )

    plt.xlabel("Solver")
    plt.ylabel("Average Search Nodes")

    plt.grid(
        axis="y",
        linestyle="--",
        alpha=0.4,
    )

    for bar, value in zip(
        bars,
        averages,
    ):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{value:.2f}",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "average_search_nodes.png",
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()


def plot_adaptive_strategy_switches(results):
    """
    Generate a graph showing the number of strategy
    switches performed by the adaptive solver for each puzzle.
    """

    adaptive_results = [
        row
        for row in results
        if row["solver"] == "adaptive"
    ]

    puzzles = [
        row["puzzle"]
        for row in adaptive_results
    ]

    switches = [
        int(row["strategy_switches"])
        for row in adaptive_results
    ]

    plt.figure(figsize=(9, 6))

    bars = plt.bar(
        puzzles,
        switches,
    )

    plt.title(
        "Adaptive Strategy Switches by Puzzle",
        fontsize=14,
        fontweight="bold",
    )

    plt.xlabel("Puzzle")
    plt.ylabel("Number of Strategy Switches")

    plt.grid(
        axis="y",
        linestyle="--",
        alpha=0.4,
    )

    for bar, value in zip(
        bars,
        switches,
    ):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            str(value),
            ha="center",
            va="bottom",
            fontsize=10,
        )

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "adaptive_strategy_switches.png",
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()


def plot_empty_cells_vs_solving_time(results):
    """
    Generate a scatter plot showing the relationship between
    the number of empty cells and solving time.
    """

    plt.figure(figsize=(9, 6))

    for solver in SOLVERS:

        solver_results = [
            row
            for row in results
            if row["solver"] == solver
        ]

        empty_cells = [
            int(row["empty_cells"])
            for row in solver_results
        ]

        solving_times = [
            float(row["solving_time"])
            for row in solver_results
        ]

        plt.scatter(
            empty_cells,
            solving_times,
            label=SOLVER_LABELS[solver],
            s=60,
        )

    plt.title(
        "Empty Cells vs Solving Time",
        fontsize=14,
        fontweight="bold",
    )

    plt.xlabel("Number of Empty Cells")
    plt.ylabel("Solving Time (seconds)")

    plt.grid(
        linestyle="--",
        alpha=0.4,
    )

    plt.legend()

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "empty_cells_vs_solving_time.png",
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()


def main():
    """Generate all benchmark visualizations."""

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

    plot_average_solving_time(results)

    plot_success_rate(results)

    plot_average_search_nodes(results)

    plot_adaptive_strategy_switches(results)

    plot_empty_cells_vs_solving_time(results)

    print()
    print("Visualization completed successfully.")
    print()
    print(f"Graphs saved to: {OUTPUT_DIR}")
    print()
    print("Generated files:")

    for file in sorted(OUTPUT_DIR.glob("*.png")):
        print(f"  {file}")


if __name__ == "__main__":
    main()