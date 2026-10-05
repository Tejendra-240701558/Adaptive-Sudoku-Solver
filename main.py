"""
Adaptive Sudoku Solver - Main Presentation Program.

Provides:
1. Interactive user Sudoku solving
2. Puzzle 7 adaptive strategy-switching demonstration
3. Complete benchmark analysis
4. Exit
"""

from benchmarks.run_benchmark import run_benchmark_analysis
from datasets.sudoku_benchmark import BENCHMARK_PUZZLES
from src.adaptive_solver import solve
from src.metrics import SolverMetrics
from src.sudoku import Sudoku
from src.user_interface import run_user_solver


def print_grid(sudoku):
    """Print a Sudoku grid in a presentation-friendly format."""

    grid = getattr(sudoku, "grid", sudoku)

    print("+-------+-------+-------+")

    for r, row in enumerate(grid):

        values = []

        for c, value in enumerate(row):

            values.append(
                str(value) if value != 0 else "."
            )

            if c in (2, 5):
                values.append("|")

        print("| " + " ".join(values) + " |")

        if r in (2, 5, 8):
            print("+-------+-------+-------+")


def run_puzzle_7_demo():
    """
    Run the Puzzle 7 presentation demonstration.

    Puzzle 7 is used because it demonstrates actual
    adaptive strategy switching.
    """

    puzzle_id = "puzzle_7"

    puzzle_data = BENCHMARK_PUZZLES[puzzle_id]

    sudoku = Sudoku(
        [row[:] for row in puzzle_data]
    )

    initial_empty = sum(
        row.count(0)
        for row in puzzle_data
    )

    print()
    print("=" * 72)
    print("             ADAPTIVE SUDOKU SOLVER - DEMONSTRATION")
    print("=" * 72)

    print(
        f"Puzzle: {puzzle_id} "
        f"({initial_empty} empty cells)"
    )

    print()
    print("Initial Puzzle:")
    print_grid(sudoku)

    metrics = SolverMetrics()

    metrics.start_timer()

    solved = solve(
        sudoku,
        metrics=metrics,
    )

    metrics.stop_timer()

    print()
    print("=" * 72)
    print("                  ADAPTIVE SOLVING RESULT")
    print("=" * 72)

    print(
        f"Status            : "
        f"{'SOLVED' if solved else 'FAILED'}"
    )

    print(
        f"Solving time      : "
        f"{metrics.solving_time:.6f} s"
    )

    print(
        f"Search nodes      : "
        f"{metrics.search_nodes}"
    )

    print(
        f"Backtracks        : "
        f"{metrics.backtracks}"
    )

    print(
        f"Conflicts         : "
        f"{metrics.conflicts}"
    )

    print(
        f"Cells solved      : "
        f"{metrics.cells_solved}"
    )

    print(
        f"Candidate reduct. : "
        f"{metrics.candidate_reductions}"
    )

    print(
        f"Strategy switches : "
        f"{metrics.strategy_switches}"
    )

    print()
    print("Strategy sequence:")

    if metrics.strategy_history:

        print(
            " -> ".join(
                metrics.strategy_history
            )
        )

    else:

        print("No strategy recorded.")

    print()
    print("Final Solution:")
    print_grid(sudoku)

    print()
    print("=" * 72)
    print("                    PRESENTATION HIGHLIGHT")
    print("=" * 72)

    print(
        "P7 demonstrates dynamic strategy switching:"
    )

    if metrics.strategy_history:

        print(
            " -> ".join(
                metrics.strategy_history
            )
        )

    else:

        print("No strategy switching occurred.")

    print(
        f"Total strategy switches: "
        f"{metrics.strategy_switches}"
    )

    print(
        f"Final result: "
        f"{'Solved' if solved else 'Not solved'}"
    )

    print("=" * 72)


def show_main_menu():
    """Display the main program menu."""

    print()
    print("=" * 72)
    print("                    ADAPTIVE SUDOKU SOLVER")
    print("=" * 72)

    print()
    print("1. Solve your own Sudoku")
    print("2. Run Puzzle 7 presentation demo")
    print("3. Run complete benchmark analysis")
    print("4. Exit")

    print()


def main():
    """Run the main Adaptive Sudoku Solver program."""

    while True:

        show_main_menu()

        choice = input(
            "Select an option (1-4): "
        ).strip()

        if choice == "1":

            run_user_solver()

        elif choice == "2":

            run_puzzle_7_demo()

        elif choice == "3":

            run_benchmark_analysis()

        elif choice == "4":

            print()
            print(
                "Exiting Adaptive Sudoku Solver."
            )
            print()

            break

        else:

            print()
            print(
                "Invalid option. "
                "Please select 1, 2, 3, or 4."
            )


if __name__ == "__main__":
    main()