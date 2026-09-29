"""
Adaptive Sudoku solver.

This module integrates Sudoku validation, puzzle analysis,
adaptive strategy selection, strategy switching, and
performance metrics into a single solving controller.
"""

from src.analyzer import analyze_puzzle
from src.constraint_propagation import propagate
from src.metrics import SolverMetrics
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


# Controlled Min-Conflicts budget used by the adaptive solver.
MIN_CONFLICTS_MAX_STEPS = 5000
MIN_CONFLICTS_MAX_RESTARTS = 2

# Short Min-Conflicts trial used when the adaptive controller
# evaluates whether local search is making useful progress.
ADAPTIVE_MIN_CONFLICTS_MAX_STEPS = 100
ADAPTIVE_MIN_CONFLICTS_MAX_RESTARTS = 1


def _run_strategy(sudoku, strategy, metrics=None):
    """
    Run one solving strategy on the given Sudoku puzzle.

    Parameters
    ----------
    sudoku : Sudoku
        Sudoku puzzle to solve.

    strategy : str
        Name of the solving strategy.

    metrics : SolverMetrics, optional
        Performance metrics object used to record solver activity.

    Returns
    -------
    bool
        True if the strategy solves the puzzle,
        otherwise False.
    """

    if strategy == CONSTRAINT_PROPAGATION:
        return propagate(
            sudoku,
            metrics=metrics,
        )

    if strategy == MRV_BACKTRACKING:
        return mrv_solve(
            sudoku,
            metrics=metrics,
        )

    if strategy == MIN_CONFLICTS:
        return min_conflicts_solve(
            sudoku,
            max_steps=ADAPTIVE_MIN_CONFLICTS_MAX_STEPS,
            max_restarts=ADAPTIVE_MIN_CONFLICTS_MAX_RESTARTS,
            metrics=metrics,
        )

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


def solve(sudoku, metrics=None):
    """
    Solve a Sudoku puzzle using adaptive strategy selection.

    The solver:
    1. Validates the initial puzzle.
    2. Analyzes its computational characteristics.
    3. Selects the initial strategy.
    4. Runs the selected strategy.
    5. Monitors solving progress.
    6. Switches strategies when sufficient progress is not made.
    7. Verifies the final solution.
    8. Records performance metrics when provided.

    Parameters
    ----------
    sudoku : Sudoku
        Sudoku puzzle to solve.

    metrics : SolverMetrics, optional
        Performance metrics object used to record
        solver activity.

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
            current_strategy,
            metrics=metrics,
        )

        # Record the number of empty cells after solving.
        after_empty = sudoku.empty_count()

        # The strategy completely solved the puzzle.
        if solved and after_empty == 0:
            return is_valid(sudoku)

        # Check whether the strategy made progress.
        if _has_sufficient_progress(
            before_empty,
            after_empty,
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
                    attempted_strategies,
                )

            if (
                next_strategy is not None
                and next_strategy != current_strategy
                and metrics is not None
            ):
                metrics.record_strategy_switch()

            current_strategy = next_strategy

            continue

        # No sufficient progress was made.
        # Switch to another unused strategy.
        next_strategy = switch_strategy(
            current_strategy,
            attempted_strategies,
        )

        if (
            next_strategy is not None
            and metrics is not None
        ):
            metrics.record_strategy_switch()

        current_strategy = next_strategy

    # All available strategies were exhausted.
    return False