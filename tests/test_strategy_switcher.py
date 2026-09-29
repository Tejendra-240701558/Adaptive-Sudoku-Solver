"""
Tests for adaptive strategy selection and switching.
"""

from src.strategy_switcher import (
    CONSTRAINT_PROPAGATION,
    MIN_CONFLICTS,
    MRV_BACKTRACKING,
    select_strategy,
    switch_strategy,
)


def test_select_constraint_propagation():
    """Select constraint propagation for propagation-friendly puzzles."""

    profile = {
        "empty_cells": 30,
        "forced_moves": 12,
        "total_candidates": 45,
        "average_candidates": 1.5,
        "maximum_candidates": 3,
        "highly_constrained_cells": 25,
    }

    strategy = select_strategy(profile)

    assert strategy == CONSTRAINT_PROPAGATION


def test_select_mrv():
    """Select MRV for moderately constrained puzzles."""

    profile = {
        "empty_cells": 40,
        "forced_moves": 5,
        "total_candidates": 120,
        "average_candidates": 3.0,
        "maximum_candidates": 6,
        "highly_constrained_cells": 15,
    }

    strategy = select_strategy(profile)

    assert strategy == MRV_BACKTRACKING


def test_select_min_conflicts():
    """
    Select Min-Conflicts for a large and highly unconstrained puzzle.

    Min-Conflicts is reserved for cases where the puzzle is
    sufficiently large and the candidate space is broad.
    """

    profile = {
        "empty_cells": 65,
        "forced_moves": 0,
        "total_candidates": 360,
        "average_candidates": 5.5,
        "maximum_candidates": 9,
        "highly_constrained_cells": 0,
    }

    strategy = select_strategy(profile)

    assert strategy == MIN_CONFLICTS


def test_switch_from_constraint_propagation():
    """Switch from constraint propagation to MRV."""

    attempted = {
        CONSTRAINT_PROPAGATION,
    }

    strategy = switch_strategy(
        CONSTRAINT_PROPAGATION,
        attempted,
    )

    assert strategy == MRV_BACKTRACKING


def test_switch_from_mrv():
    """Switch from MRV to constraint propagation when available."""

    attempted = {
        MRV_BACKTRACKING,
    }

    strategy = switch_strategy(
        MRV_BACKTRACKING,
        attempted,
    )

    assert strategy == CONSTRAINT_PROPAGATION


def test_switch_to_min_conflicts():
    """Select Min-Conflicts when the other strategies were attempted."""

    attempted = {
        CONSTRAINT_PROPAGATION,
        MRV_BACKTRACKING,
    }

    strategy = switch_strategy(
        MRV_BACKTRACKING,
        attempted,
    )

    assert strategy == MIN_CONFLICTS


def test_switch_returns_none_when_all_attempted():
    """Return None when every strategy has already been attempted."""

    attempted = {
        CONSTRAINT_PROPAGATION,
        MRV_BACKTRACKING,
        MIN_CONFLICTS,
    }

    strategy = switch_strategy(
        MRV_BACKTRACKING,
        attempted,
    )

    assert strategy is None