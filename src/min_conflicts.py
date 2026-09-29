"""
Min-Conflicts local search solver for Sudoku.

This module solves Sudoku using local search by repeatedly
changing the value of a conflicted cell to a value that
minimizes the number of constraint conflicts.
"""

import random

from src.sudoku import Sudoku


def _conflict_count(sudoku, row, col, value):
    """
    Count the number of conflicts produced by placing a value
    in the specified cell.

    The current value of the cell is ignored while checking
    the row, column, and subgrid.
    """

    conflicts = 0

    # Check row.
    for current_col in range(Sudoku.SIZE):
        if current_col != col:
            if sudoku.grid[row][current_col] == value:
                conflicts += 1

    # Check column.
    for current_row in range(Sudoku.SIZE):
        if current_row != row:
            if sudoku.grid[current_row][col] == value:
                conflicts += 1

    # Check 3x3 subgrid.
    start_row = (row // Sudoku.SUBGRID_SIZE) * Sudoku.SUBGRID_SIZE
    start_col = (col // Sudoku.SUBGRID_SIZE) * Sudoku.SUBGRID_SIZE

    for current_row in range(
        start_row,
        start_row + Sudoku.SUBGRID_SIZE
    ):
        for current_col in range(
            start_col,
            start_col + Sudoku.SUBGRID_SIZE
        ):
            if current_row == row and current_col == col:
                continue

            if sudoku.grid[current_row][current_col] == value:
                conflicts += 1

    return conflicts


def _initialize_grid(sudoku, rng):
    """
    Fill all empty cells with random values from 1 to 9.

    Original fixed cells are not changed.
    """

    for row, col in sudoku.empty_cells():
        sudoku.set(row, col, rng.randint(1, Sudoku.SIZE))


def _get_conflicted_cells(sudoku, mutable_cells):
    """
    Return mutable cells that currently contain conflicts.
    """

    conflicted = []

    for row, col in mutable_cells:
        value = sudoku.get(row, col)

        if _conflict_count(sudoku, row, col, value) > 0:
            conflicted.append((row, col))

    return conflicted


def solve(
    sudoku,
    max_steps=100000,
    seed=42,
    max_restarts=10,
    metrics=None,
):
    """
    Solve Sudoku using the Min-Conflicts local-search algorithm.

    Parameters
    ----------
    sudoku : Sudoku
        Sudoku puzzle to solve.

    max_steps : int
        Maximum number of local-search steps per restart.

    seed : int
        Random seed used for reproducible results.

    max_restarts : int
        Number of random restarts allowed.

    metrics : SolverMetrics, optional
        Performance metrics object used to record solver activity.

    Returns
    -------
    bool
        True if a solution is found, otherwise False.
    """

    original = sudoku.copy()
    mutable_cells = original.empty_cells()

    # A completely filled puzzle is already solved.
    if not mutable_cells:
        return True

    rng = random.Random(seed)

    for _ in range(max_restarts):

        # Restore the original puzzle before each restart.
        sudoku.grid = [
            row.copy()
            for row in original.grid
        ]

        # Create a complete candidate assignment.
        _initialize_grid(sudoku, rng)

        for _ in range(max_steps):

            # Record one local-search step.
            if metrics is not None:
                metrics.record_search_node()

            conflicted_cells = _get_conflicted_cells(
                sudoku,
                mutable_cells
            )

            # No conflicts means the Sudoku is solved.
            if not conflicted_cells:
                if metrics is not None:
                    for _ in mutable_cells:
                        metrics.record_cell_solved()

                return True

            # Record the number of currently conflicted cells.
            if metrics is not None:
                for _ in conflicted_cells:
                    metrics.record_conflict()

            # Choose one conflicted cell randomly.
            row, col = rng.choice(conflicted_cells)

            # Calculate conflicts for every possible value.
            conflict_values = []

            for value in range(1, Sudoku.SIZE + 1):

                conflicts = _conflict_count(
                    sudoku,
                    row,
                    col,
                    value
                )

                conflict_values.append(
                    (value, conflicts)
                )

            minimum_conflicts = min(
                conflicts
                for _, conflicts in conflict_values
            )

            # Randomly choose among equally good values.
            best_values = [
                value
                for value, conflicts in conflict_values
                if conflicts == minimum_conflicts
            ]

            value = rng.choice(best_values)

            sudoku.set(row, col, value)

    # Restore the original puzzle if no solution was found.
    sudoku.grid = [
        row.copy()
        for row in original.grid
    ]

    return False