"""
Sudoku grid representation.

This module provides the basic Sudoku data structure used by
the validator, candidate generator, solvers, analyzer, and
adaptive solver.
"""


class Sudoku:
    """Represent a standard 9x9 Sudoku puzzle."""

    SIZE = 9
    SUBGRID_SIZE = 3
    EMPTY = 0

    def __init__(self, grid):
        """
        Initialize a Sudoku puzzle.

        Parameters
        ----------
        grid : list[list[int]]
            A 9x9 Sudoku grid where 0 represents an empty cell.
        """

        if len(grid) != self.SIZE:
            raise ValueError("Sudoku grid must contain exactly 9 rows.")

        if any(len(row) != self.SIZE for row in grid):
            raise ValueError("Each Sudoku row must contain exactly 9 values.")

        self.grid = [row.copy() for row in grid]

    def get(self, row, col):
        """Return the value at the specified cell."""
        self._check_position(row, col)
        return self.grid[row][col]

    def set(self, row, col, value):
        """Set a value at the specified cell."""
        self._check_position(row, col)

        if not 0 <= value <= 9:
            raise ValueError("Sudoku values must be between 0 and 9.")

        self.grid[row][col] = value

    def is_empty(self, row, col):
        """Return True if the specified cell is empty."""
        return self.get(row, col) == self.EMPTY

    def empty_cells(self):
        """Return a list of all empty cell positions."""
        cells = []

        for row in range(self.SIZE):
            for col in range(self.SIZE):
                if self.grid[row][col] == self.EMPTY:
                    cells.append((row, col))

        return cells

    def empty_count(self):
        """Return the number of empty cells."""
        return len(self.empty_cells())

    def copy(self):
        """Return an independent copy of the Sudoku puzzle."""
        return Sudoku(self.grid)

    def _check_position(self, row, col):
        """Check whether a cell position is valid."""
        if not (0 <= row < self.SIZE and 0 <= col < self.SIZE):
            raise IndexError("Sudoku position must be between 0 and 8.")

    def display(self):
        """Display the Sudoku grid in a readable format."""
        for row in self.grid:
            print(" ".join(str(value) for value in row))

    def __str__(self):
        """Return the Sudoku grid as a string."""
        return "\n".join(
            " ".join(str(value) for value in row)
            for row in self.grid
        )