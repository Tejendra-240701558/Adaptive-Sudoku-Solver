"""Sudoku puzzle analysis and computational profiling."""
"""
Sudoku puzzle analyzer.

This module extracts measurable characteristics from a Sudoku
puzzle and creates a computational profile for adaptive solving.
"""

from src.candidates import get_all_candidates


def analyze_puzzle(sudoku):
    """
    Analyze the current Sudoku puzzle.

    Parameters
    ----------
    sudoku : Sudoku
        Sudoku puzzle to analyze.

    Returns
    -------
    dict
        Computational profile containing measurable
        characteristics of the puzzle.
    """

    candidates = get_all_candidates(sudoku)

    empty_cells = sudoku.empty_count()

    candidate_counts = [
        len(values)
        for values in candidates.values()
    ]

    forced_moves = sum(
        1
        for count in candidate_counts
        if count == 1
    )

    total_candidates = sum(candidate_counts)

    if candidate_counts:
        average_candidates = (
            total_candidates / len(candidate_counts)
        )
        maximum_candidates = max(candidate_counts)
    else:
        average_candidates = 0.0
        maximum_candidates = 0

    highly_constrained_cells = sum(
        1
        for count in candidate_counts
        if count <= 2
    )

    return {
        "empty_cells": empty_cells,
        "forced_moves": forced_moves,
        "total_candidates": total_candidates,
        "average_candidates": average_candidates,
        "maximum_candidates": maximum_candidates,
        "highly_constrained_cells": highly_constrained_cells,
    }