"""
Inspect adaptive strategy histories for benchmark puzzles.
"""

from datasets.generate_benchmark import generate_dataset
from src.adaptive_solver import solve
from src.metrics import SolverMetrics
from src.sudoku import Sudoku


def main():
    """Display adaptive strategy history for every puzzle."""

    dataset = generate_dataset()

    for name, puzzle in dataset.items():

        sudoku = Sudoku(puzzle)
        metrics = SolverMetrics()

        metrics.start_timer()

        solved = solve(
            sudoku,
            metrics=metrics,
        )

        metrics.stop_timer()

        print(
            f"{name}: "
            f"solved={solved} "
            f"time={metrics.solving_time:.6f}s "
            f"history={metrics.strategy_history} "
            f"switches={metrics.strategy_switches}"
        )


if __name__ == "__main__":
    main()