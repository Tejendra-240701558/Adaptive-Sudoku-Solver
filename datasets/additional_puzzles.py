"""
Additional Sudoku puzzles for interactive testing.

These puzzles are kept separate from the official benchmark
dataset so that the existing benchmark results remain unchanged.

Puzzle 9 is intended for testing adaptive strategy selection
and strategy switching.
"""

ADDITIONAL_PUZZLES = {
    "puzzle_9": [
        [0, 0, 4, 6, 0, 0, 9, 0, 0],
        [0, 0, 0, 0, 0, 0, 3, 0, 0],
        [0, 0, 0, 0, 0, 2, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 2, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 9, 0, 0, 8, 0, 0],
        [0, 0, 1, 0, 3, 0, 2, 0, 0],
        [2, 0, 0, 0, 0, 0, 0, 0, 5],
        [0, 4, 0, 0, 0, 6, 0, 7, 0],
    ]
}


def get_puzzle(puzzle_id):
    """
    Return an independent copy of an additional Sudoku puzzle.
    """

    if puzzle_id not in ADDITIONAL_PUZZLES:
        raise KeyError(
            f"Unknown additional puzzle: {puzzle_id}"
        )

    return [
        row.copy()
        for row in ADDITIONAL_PUZZLES[puzzle_id]
    ]