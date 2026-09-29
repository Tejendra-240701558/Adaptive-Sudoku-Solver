"""
Performance metrics for Sudoku solvers.

This module provides a common structure for recording
and reporting solver performance.
"""

from dataclasses import dataclass, asdict, field
from time import perf_counter


@dataclass
class SolverMetrics:
    """Store performance statistics for a Sudoku solver."""

    solving_time: float = 0.0
    search_nodes: int = 0
    backtracks: int = 0
    conflicts: int = 0
    cells_solved: int = 0
    candidate_reductions: int = 0
    strategy_switches: int = 0
    strategy_history: list[str] = field(default_factory=list)

    def start_timer(self):
        """Start the performance timer."""
        self._start_time = perf_counter()

    def stop_timer(self):
        """Stop the timer and store the elapsed time."""
        if hasattr(self, "_start_time"):
            self.solving_time = perf_counter() - self._start_time

    def record_search_node(self):
        """Record one explored search node."""
        self.search_nodes += 1

    def record_backtrack(self):
        """Record one backtracking operation."""
        self.backtracks += 1

    def record_conflict(self):
        """Record one constraint conflict."""
        self.conflicts += 1

    def record_cell_solved(self):
        """Record one solved cell."""
        self.cells_solved += 1

    def record_candidate_reduction(self, count=1):
        """Record candidate-value reductions."""
        self.candidate_reductions += count

    def record_strategy_switch(self):
        """Record one strategy switch."""
        self.strategy_switches += 1

    def record_strategy(self, strategy):
        """
        Record a strategy used by the adaptive solver.

        Duplicate consecutive strategy entries are ignored so
        that the history represents actual strategy changes.
        """

        if not self.strategy_history:
            self.strategy_history.append(strategy)
            return

        if self.strategy_history[-1] != strategy:
            self.strategy_history.append(strategy)

    def to_dict(self):
        """Return the metrics as a dictionary."""
        return asdict(self)