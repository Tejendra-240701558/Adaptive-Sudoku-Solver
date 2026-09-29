from src.metrics import SolverMetrics


def test_metrics_initial_values():
    metrics = SolverMetrics()

    assert metrics.solving_time == 0.0
    assert metrics.search_nodes == 0
    assert metrics.backtracks == 0
    assert metrics.conflicts == 0
    assert metrics.cells_solved == 0
    assert metrics.candidate_reductions == 0
    assert metrics.strategy_switches == 0


def test_metrics_recording():
    metrics = SolverMetrics()

    metrics.record_search_node()
    metrics.record_search_node()

    metrics.record_backtrack()

    metrics.record_conflict()
    metrics.record_conflict()

    metrics.record_cell_solved()

    metrics.record_candidate_reduction()
    metrics.record_candidate_reduction(3)

    metrics.record_strategy_switch()

    assert metrics.search_nodes == 2
    assert metrics.backtracks == 1
    assert metrics.conflicts == 2
    assert metrics.cells_solved == 1
    assert metrics.candidate_reductions == 4
    assert metrics.strategy_switches == 1


def test_metrics_to_dict():
    metrics = SolverMetrics()

    metrics.record_search_node()
    metrics.record_backtrack()

    data = metrics.to_dict()

    assert data["search_nodes"] == 1
    assert data["backtracks"] == 1
    assert data["conflicts"] == 0
    assert data["cells_solved"] == 0