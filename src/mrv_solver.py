"""
MRV-based Sudoku solver.

This module combines the Minimum Remaining Values (MRV)
heuristic with recursive backtracking.
"""

from src.candidates import get_candidates
from src.mrv import select_mrv_cell


def solve(sudoku):
    """
    Solve a Sudoku puzzle using MRV and backtracking.

    Parameters
    ----------
    sudoku : Sudoku
        Sudoku puzzle to solve.

    Returns
    -------
    bool
        True if a solution is found, otherwise False.
    """

    # If there are no empty cells, the puzzle is solved.
    if not sudoku.empty_cells():
        return True

    # Select the most constrained empty cell.
    cell = select_mrv_cell(sudoku)

    if cell is None:
        return True

    row, col = cell

    candidates = get_candidates(sudoku, row, col)

    # No candidates means this branch is contradictory.
    if not candidates:
        return False

    # Try each candidate recursively.
    for value in candidates:
        sudoku.set(row, col, value)

        if solve(sudoku):
            return True

        # Undo the choice if it leads to a dead end.
        sudoku.set(row, col, sudoku.EMPTY)

    return False