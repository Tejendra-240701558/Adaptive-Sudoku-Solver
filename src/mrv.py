"""
Minimum Remaining Values (MRV) heuristic for Sudoku.

This module selects the empty Sudoku cell with the
fewest possible candidate values.
"""

from src.candidates import get_candidates


def select_mrv_cell(sudoku):
    """
    Select the empty cell with the fewest candidates.

    Parameters
    ----------
    sudoku : Sudoku
        Sudoku puzzle.

    Returns
    -------
    tuple or None
        The (row, column) position with the fewest candidates.
        Returns None if there are no empty cells.
    """

    best_cell = None
    fewest_candidates = None

    for row, col in sudoku.empty_cells():
        candidates = get_candidates(sudoku, row, col)

        if fewest_candidates is None or len(candidates) < fewest_candidates:
            fewest_candidates = len(candidates)
            best_cell = (row, col)

    return best_cell