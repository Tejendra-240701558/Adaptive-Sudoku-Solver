"""
Basic backtracking solver for Sudoku.

This module solves Sudoku puzzles using recursive
depth-first search and backtracking.
"""

from src.candidates import get_candidates


def solve(sudoku):
    """
    Solve a Sudoku puzzle using basic backtracking.

    Parameters
    ----------
    sudoku : Sudoku
        Sudoku puzzle to solve.

    Returns
    -------
    bool
        True if a solution is found, otherwise False.
    """

    empty_cells = sudoku.empty_cells()

    # No empty cells means the puzzle is solved.
    if not empty_cells:
        return True

    # Select the first empty cell.
    row, col = empty_cells[0]

    # Try every valid candidate.
    candidates = get_candidates(sudoku, row, col)

    for value in candidates:
        sudoku.set(row, col, value)

        # Recursively continue solving.
        if solve(sudoku):
            return True

        # The choice led to a dead end.
        # Reset the cell and try another candidate.
        sudoku.set(row, col, sudoku.EMPTY)

    return False