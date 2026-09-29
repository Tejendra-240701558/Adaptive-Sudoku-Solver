"""
Constraint propagation for Sudoku.

This module repeatedly fills cells that have exactly one
possible candidate.
"""

from src.candidates import get_candidates


def propagate(sudoku):
    """
    Apply constraint propagation using naked singles.

    The process continues until no more cells can be solved
    using a single candidate.

    Parameters
    ----------
    sudoku : Sudoku
        Sudoku puzzle to solve.

    Returns
    -------
    bool
        True if propagation completes without contradiction.
        False if an empty cell has no possible candidates.
    """

    progress = True

    while progress:
        progress = False

        for row, col in sudoku.empty_cells():
            candidates = get_candidates(sudoku, row, col)

            # No candidate means the current state is contradictory.
            if not candidates:
                return False

            # Exactly one candidate means the value is forced.
            if len(candidates) == 1:
                value = next(iter(candidates))
                sudoku.set(row, col, value)
                progress = True

    return True