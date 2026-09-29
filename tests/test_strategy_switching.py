from src.strategy_switcher import (
    switch_strategy,
    CONSTRAINT_PROPAGATION,
    MRV_BACKTRACKING,
    MIN_CONFLICTS,
)


def test_switch_from_constraint_propagation():
    attempted_strategies = {
        CONSTRAINT_PROPAGATION
    }

    next_strategy = switch_strategy(
        CONSTRAINT_PROPAGATION,
        attempted_strategies
    )

    assert next_strategy == MRV_BACKTRACKING


def test_switch_from_mrv_backtracking():
    attempted_strategies = {
        CONSTRAINT_PROPAGATION,
        MRV_BACKTRACKING
    }

    next_strategy = switch_strategy(
        MRV_BACKTRACKING,
        attempted_strategies
    )

    assert next_strategy == MIN_CONFLICTS


def test_switch_from_min_conflicts():
    attempted_strategies = {
        CONSTRAINT_PROPAGATION,
        MRV_BACKTRACKING,
        MIN_CONFLICTS
    }

    next_strategy = switch_strategy(
        MIN_CONFLICTS,
        attempted_strategies
    )

    assert next_strategy is None


def test_switch_skips_attempted_strategy():
    attempted_strategies = {
        CONSTRAINT_PROPAGATION,
        MIN_CONFLICTS
    }

    next_strategy = switch_strategy(
        CONSTRAINT_PROPAGATION,
        attempted_strategies
    )

    assert next_strategy == MRV_BACKTRACKING