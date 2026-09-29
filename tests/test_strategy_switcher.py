from src.strategy_switcher import (
    select_strategy,
    CONSTRAINT_PROPAGATION,
    MRV_BACKTRACKING,
    MIN_CONFLICTS,
)


def test_select_constraint_propagation():
    profile = {
        "empty_cells": 45,
        "forced_moves": 5,
        "total_candidates": 100,
        "average_candidates": 2.2,
        "maximum_candidates": 4,
        "highly_constrained_cells": 10,
    }

    strategy = select_strategy(profile)

    assert strategy == CONSTRAINT_PROPAGATION


def test_select_mrv_backtracking():
    profile = {
        "empty_cells": 30,
        "forced_moves": 0,
        "total_candidates": 75,
        "average_candidates": 2.5,
        "maximum_candidates": 4,
        "highly_constrained_cells": 0,
    }

    strategy = select_strategy(profile)

    assert strategy == MRV_BACKTRACKING


def test_select_min_conflicts():
    profile = {
        "empty_cells": 50,
        "forced_moves": 0,
        "total_candidates": 200,
        "average_candidates": 4.0,
        "maximum_candidates": 7,
        "highly_constrained_cells": 0,
    }

    strategy = select_strategy(profile)

    assert strategy == MIN_CONFLICTS


def test_default_strategy():
    profile = {
        "empty_cells": 20,
        "forced_moves": 0,
        "total_candidates": 70,
        "average_candidates": 3.5,
        "maximum_candidates": 5,
        "highly_constrained_cells": 0,
    }

    strategy = select_strategy(profile)

    assert strategy == MRV_BACKTRACKING