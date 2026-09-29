from datasets.sudoku_benchmark import BENCHMARK_PUZZLES
from src.mrv_solver import solve
from src.sudoku import Sudoku
from src.validator import is_valid


def test_all_benchmark_puzzles_are_solvable():
    for puzzle_name, puzzle in BENCHMARK_PUZZLES.items():
        sudoku = Sudoku(puzzle)

        solved = solve(sudoku)

        assert solved is True, (
            f"{puzzle_name} could not be solved."
        )

        assert sudoku.empty_count() == 0, (
            f"{puzzle_name} still has empty cells."
        )

        assert is_valid(sudoku), (
            f"{puzzle_name} produced an invalid solution."
        )