"""
User interface for the Adaptive Sudoku Solver.

This module allows a user to enter a Sudoku puzzle as a
9x9 matrix and solve it using the existing adaptive solver.
"""

from src.adaptive_solver import solve
from src.metrics import SolverMetrics
from src.sudoku import Sudoku
from src.validator import is_valid


def read_sudoku_from_user():
    """
    Read a 9x9 Sudoku matrix from the user.

    The user must enter one row at a time.
    Use 0 to represent an empty cell.

    Returns
    -------
    Sudoku
        Sudoku object created from the user's input.
    """

    print()
    print("=" * 60)
    print("              ADAPTIVE SUDOKU SOLVER")
    print("=" * 60)
    print()
    print("Enter the Sudoku puzzle row by row.")
    print("Use numbers 1-9 for filled cells and 0 for empty cells.")
    print("Enter exactly 9 numbers in each row.")
    print()

    grid = []

    for row_number in range(1, 10):

        while True:

            user_input = input(
                f"Row {row_number}: "
            ).strip()

            values = user_input.split()

            if len(values) != 9:
                print(
                    "Error: Enter exactly 9 numbers separated by spaces."
                )
                continue

            try:
                row = [int(value) for value in values]
            except ValueError:
                print(
                    "Error: Only integers from 0 to 9 are allowed."
                )
                continue

            if any(value < 0 or value > 9 for value in row):
                print(
                    "Error: Values must be between 0 and 9."
                )
                continue

            grid.append(row)
            break

    return Sudoku(grid)


def display_solution(sudoku):
    """
    Display a Sudoku grid in a readable format.
    """

    print()
    print("=" * 25)
    print("       SOLVED SUDOKU")
    print("=" * 25)

    for row in sudoku.grid:
        print(" ".join(str(value) for value in row))

    print("=" * 25)


def run_user_solver():
    """
    Run the interactive user-solving mode.
    """

    sudoku = read_sudoku_from_user()

    print()
    print("Validating Sudoku puzzle...")

    if not is_valid(sudoku):
        print()
        print("Invalid Sudoku puzzle.")
        print(
            "The puzzle contains duplicate or invalid values "
            "in a row, column, or 3x3 subgrid."
        )
        return

    print("Puzzle validation successful.")

    metrics = SolverMetrics()
    metrics.start_timer()

    solved = solve(
        sudoku,
        metrics=metrics,
    )

    metrics.stop_timer()

    if solved and is_valid(sudoku) and not sudoku.empty_cells():

        print()
        print("Solution found successfully.")

        display_solution(sudoku)

        print()
        print("=" * 60)
        print("              SOLVING INFORMATION")
        print("=" * 60)

        print(
            f"Strategies used     : "
            f"{' -> '.join(metrics.strategy_history)}"
        )

        print(
            f"Strategy switches   : "
            f"{metrics.strategy_switches}"
        )

        print(
            f"Search nodes        : "
            f"{metrics.search_nodes}"
        )

        print(
            f"Backtracks          : "
            f"{metrics.backtracks}"
        )

        print(
            f"Conflicts           : "
            f"{metrics.conflicts}"
        )

        print(
            f"Cells solved        : "
            f"{metrics.cells_solved}"
        )

        print(
            f"Solving time        : "
            f"{metrics.solving_time:.6f} seconds"
        )

        print("=" * 60)

    else:

        print()
        print("The Adaptive Sudoku Solver could not solve this puzzle.")
        print(
            "The available solving strategies were exhausted "
            "without obtaining a verified solution."
        )