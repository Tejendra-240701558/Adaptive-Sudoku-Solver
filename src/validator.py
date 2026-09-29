"""
Sudoku validation functions.

This module checks whether a Sudoku puzzle has a valid structure,
valid values, and no duplicate values in rows, columns, or 3x3 subgrids.
"""

from src.sudoku import Sudoku


def validate_grid_structure(sudoku):
    """Check that the object contains a valid 9x9 Sudoku grid."""

    if not isinstance(sudoku, Sudoku):
        raise TypeError("Expected a Sudoku object.")

    if len(sudoku.grid) != Sudoku.SIZE:
        return False

    if any(len(row) != Sudoku.SIZE for row in sudoku.grid):
        return False

    return True


def validate_values(sudoku):
    """Check that every cell contains a value from 0 to 9."""

    for row in sudoku.grid:
        for value in row:
            if not isinstance(value, int):
                return False

            if not 0 <= value <= 9:
                return False

    return True


def validate_rows(sudoku):
    """Check that no row contains duplicate non-zero values."""

    for row in sudoku.grid:
        values = [value for value in row if value != Sudoku.EMPTY]

        if len(values) != len(set(values)):
            return False

    return True


def validate_columns(sudoku):
    """Check that no column contains duplicate non-zero values."""

    for col in range(Sudoku.SIZE):
        values = [
            sudoku.grid[row][col]
            for row in range(Sudoku.SIZE)
            if sudoku.grid[row][col] != Sudoku.EMPTY
        ]

        if len(values) != len(set(values)):
            return False

    return True


def validate_subgrids(sudoku):
    """Check that no 3x3 subgrid contains duplicate non-zero values."""

    for start_row in range(0, Sudoku.SIZE, Sudoku.SUBGRID_SIZE):
        for start_col in range(0, Sudoku.SIZE, Sudoku.SUBGRID_SIZE):

            values = []

            for row in range(
                start_row,
                start_row + Sudoku.SUBGRID_SIZE
            ):
                for col in range(
                    start_col,
                    start_col + Sudoku.SUBGRID_SIZE
                ):
                    value = sudoku.grid[row][col]

                    if value != Sudoku.EMPTY:
                        values.append(value)

            if len(values) != len(set(values)):
                return False

    return True


def is_valid(sudoku):
    """
    Check whether a Sudoku puzzle is valid.

    A valid puzzle must satisfy:
    - Correct 9x9 structure
    - Values between 0 and 9
    - No duplicate values in rows
    - No duplicate values in columns
    - No duplicate values in 3x3 subgrids
    """

    return (
        validate_grid_structure(sudoku)
        and validate_values(sudoku)
        and validate_rows(sudoku)
        and validate_columns(sudoku)
        and validate_subgrids(sudoku)
    )