"""
Adaptive Sudoku Solver - Presentation Demo.

Runs the adaptive solver on benchmark Puzzle 7,
which demonstrates strategy switching.
"""

from datasets.sudoku_benchmark import BENCHMARK_PUZZLES
from src.adaptive_solver import solve
from src.metrics import SolverMetrics
from src.sudoku import Sudoku


def print_grid(sudoku):
    """Print Sudoku grid in a presentation-friendly format."""

    grid = getattr(sudoku, "grid", sudoku)

    print("+-------+-------+-------+")

    for r, row in enumerate(grid):

        values = []

        for c, value in enumerate(row):

            values.append(str(value) if value != 0 else ".")

            if c in (2, 5):
                values.append("|")

        print("| " + " ".join(values) + " |")

        if r in (2, 5, 8):
            print("+-------+-------+-------+")


def main():

    # --------------------------------------------------------
    # Select P7
    # --------------------------------------------------------

    puzzle_id = "puzzle_7"

    puzzle_data = BENCHMARK_PUZZLES[puzzle_id]

    sudoku = Sudoku([row[:] for row in puzzle_data])

    initial_empty = sum(row.count(0) for row in puzzle_data)

    # --------------------------------------------------------
    # Header
    # --------------------------------------------------------

    print("=" * 72)
    print("ADAPTIVE SUDOKU SOLVER - LIVE DEMONSTRATION")
    print("=" * 72)

    print(f"Puzzle: {puzzle_id} ({initial_empty} empty cells)")

    # --------------------------------------------------------
    # Initial puzzle
    # --------------------------------------------------------

    print("\nInitial Puzzle:")
    print_grid(sudoku)

    # --------------------------------------------------------
    # Run adaptive solver
    # --------------------------------------------------------

    metrics = SolverMetrics()

    solved = solve(sudoku, metrics)

    # --------------------------------------------------------
    # Results
    # --------------------------------------------------------

    print("\n" + "=" * 72)
    print("ADAPTIVE SOLVING RESULT")
    print("=" * 72)

    print(f"Status            : {'SOLVED' if solved else 'FAILED'}")
    print(f"Solving time      : {metrics.solving_time:.6f} s")
    print(f"Search nodes      : {metrics.search_nodes}")
    print(f"Backtracks        : {metrics.backtracks}")
    print(f"Conflicts         : {metrics.conflicts}")
    print(f"Cells solved      : {metrics.cells_solved}")
    print(f"Candidate reduct. : {metrics.candidate_reductions}")
    print(f"Strategy switches : {metrics.strategy_switches}")

    # --------------------------------------------------------
    # Strategy history
    # --------------------------------------------------------

    print("\nStrategy sequence:")

    if metrics.strategy_history:
        print(" -> ".join(metrics.strategy_history))
    else:
        print("No strategy recorded.")

    # --------------------------------------------------------
    # Final solution
    # --------------------------------------------------------

    print("\nFinal Solution:")
    print_grid(sudoku)

    # --------------------------------------------------------
    # Presentation highlight
    # --------------------------------------------------------

    print("\n" + "=" * 72)
    print("PRESENTATION HIGHLIGHT")
    print("=" * 72)

    print("P7 demonstrates dynamic strategy switching:")
    print("Min-Conflicts -> Constraint Propagation -> MRV + Backtracking")

    print(f"Total strategy switches: {metrics.strategy_switches}")
    print(f"Final result: {'Solved' if solved else 'Not solved'}")

    print("=" * 72)


if __name__ == "__main__":
    main()
