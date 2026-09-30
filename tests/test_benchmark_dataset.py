from datasets.sudoku_benchmark import BENCHMARK_PUZZLES
from src.sudoku import Sudoku
from src.validator import is_valid


def test_benchmark_dataset_contains_eight_puzzles():
    assert len(BENCHMARK_PUZZLES) == 8

    expected_puzzles = {
        "puzzle_1",
        "puzzle_2",
        "puzzle_3",
        "puzzle_4",
        "puzzle_5",
        "puzzle_6",
        "puzzle_7",
        "puzzle_8",
    }

    assert set(BENCHMARK_PUZZLES.keys()) == expected_puzzles
    

def test_all_benchmark_puzzles_have_nine_rows():
    for puzzle in BENCHMARK_PUZZLES.values():
        assert len(puzzle) == 9


def test_all_benchmark_puzzles_have_nine_columns():
    for puzzle in BENCHMARK_PUZZLES.values():
        for row in puzzle:
            assert len(row) == 9


def test_all_benchmark_puzzles_have_valid_values():
    for puzzle in BENCHMARK_PUZZLES.values():
        sudoku = Sudoku(puzzle)

        assert is_valid(sudoku)