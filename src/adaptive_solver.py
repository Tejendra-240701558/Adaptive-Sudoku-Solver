"""
Adaptive Sudoku solver.

This module integrates Sudoku validation, puzzle analysis,
adaptive strategy selection, and strategy switching into
a single solving controller.
"""

from src.analyzer import analyze_puzzle
from src.constraint_propagation import propagate
from src.min_conflicts import solve as min_conflicts_solve
from src.mrv_solver import solve as mrv_solve
from src.strategy_switcher import (
    CONSTRAINT_PROPAGATION,
    MRV_BACKTRACKING,
    MIN_CONFLICTS,
    select_strategy,
    switch_strategy,
)
from src.validator import is_valid


def _run_strategy(sudoku, strategy):
    """
    Run one solving strategy on the given Sudoku puzzle.

    Parameters
    ----------
    sudoku : Sudoku
        Sudoku puzzle to solve.

    strategy : str
        Name of the solving strategy.

    Returns
    -------
    bool
        True if the strategy solves the puzzle,
        otherwise False.
    """

    if strategy == CONSTRAINT_PROPAGATION:
        return propagate(sudoku)

    if strategy == MRV_BACKTRACKING:
        return mrv_solve(sudoku)

    if strategy == MIN_CONFLICTS:
        return min_conflicts_solve(sudoku)

    raise ValueError(
        f"Unknown solving strategy: {strategy}"
    )


def _has_sufficient_progress(before, after):
    """
    Check whether the solving attempt made progress.

    Progress is measured by comparing the number of empty
    cells before and after the strategy execution.

    Parameters
    ----------
    before : int
        Number of empty cells before the strategy.

    after : int
        Number of empty cells after the strategy.

    Returns
    -------
    bool
        True if the number of empty cells decreased.
    """

    return after < before


def solve(sudoku):
    """
    Solve a Sudoku puzzle using adaptive strategy selection.

    The solver:
    1. Validates the input puzzle.
    2. Analyzes its computational characteristics.
    3. Selects an initial strategy.
    4. Runs the selected strategy.
    5. Switches strategies when sufficient progress is not made.
    6. Verifies the final solution.

    Parameters
    ----------
    sudoku : Sudoku
        Sudoku puzzle to solve.

    Returns
    -------
    bool
        True if the puzzle is solved successfully,
        otherwise False.
    """

    # Validate the initial Sudoku puzzle.
    if not is_valid(sudoku):
        return False

    # If there are no empty cells, the puzzle is already solved.
    if not sudoku.empty_cells():
        return True

    # Analyze the initial puzzle.
    profile = analyze_puzzle(sudoku)

    # Select the initial strategy.
    current_strategy = select_strategy(profile)

    # Keep track of strategies already attempted.
    attempted_strategies = set()

    while current_strategy is not None:

        attempted_strategies.add(current_strategy)

        # Record the number of empty cells before solving.
        before_empty = sudoku.empty_count()

        # Run the selected strategy.
        solved = _run_strategy(
            sudoku,
            current_strategy
        )

        # Record the number of empty cells after solving.
        after_empty = sudoku.empty_count()

        # The strategy completely solved the puzzle.
        if solved and after_empty == 0:
            return is_valid(sudoku)

        # Check whether the strategy made progress.
        if _has_sufficient_progress(
            before_empty,
            after_empty
        ):
            # Re-analyze the updated Sudoku state.
            profile = analyze_puzzle(sudoku)

            # Select a strategy for the new state.
            next_strategy = select_strategy(profile)

            # If the selected strategy was already attempted,
            # choose another unused strategy.
            if next_strategy in attempted_strategies:
                next_strategy = switch_strategy(
                    next_strategy,
                    attempted_strategies
                )

            current_strategy = next_strategy

            continue

        # No sufficient progress was made.
        # Switch to another unused strategy.
        current_strategy = switch_strategy(
            current_strategy,
            attempted_strategies
        )

    # All available strategies were exhausted.
    return False