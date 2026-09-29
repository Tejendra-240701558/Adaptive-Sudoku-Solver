"""
Sudoku candidate generation.

This module determines which values can legally be placed
in empty Sudoku cells.
"""

from src.sudoku import Sudoku


def get_candidates(sudoku, row, col):
    """
    Return all valid candidate values for an empty cell.
    """

    if not sudoku.is_empty(row, col):
        return set()

    candidates = set(range(1, Sudoku.SIZE + 1))

    # Remove values already present in the row.
    for value in sudoku.grid[row]:
        candidates.discard(value)

    # Remove values already present in the column.
    for r in range(Sudoku.SIZE):
        candidates.discard(sudoku.grid[r][col])

    # Find the 3x3 subgrid containing the cell.
    start_row = (row // Sudoku.SUBGRID_SIZE) * Sudoku.SUBGRID_SIZE
    start_col = (col // Sudoku.SUBGRID_SIZE) * Sudoku.SUBGRID_SIZE

    for r in range(
        start_row,
        start_row + Sudoku.SUBGRID_SIZE
    ):
        for c in range(
            start_col,
            start_col + Sudoku.SUBGRID_SIZE
        ):
            candidates.discard(sudoku.grid[r][c])

    return candidates


def get_all_candidates(sudoku):
    """
    Return candidates for every empty cell.

    Returns
    -------
    dict
        Dictionary where the key is the cell position
        (row, column) and the value is its candidate set.
    """

    all_candidates = {}

    for row in range(Sudoku.SIZE):
        for col in range(Sudoku.SIZE):
            if sudoku.is_empty(row, col):
                all_candidates[(row, col)] = get_candidates(
                    sudoku,
                    row,
                    col
                )

    return all_candidates