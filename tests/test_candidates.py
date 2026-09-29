from src.sudoku import Sudoku
from src.candidates import get_candidates, get_all_candidates


def test_candidates_for_empty_cell():
    puzzle = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 0],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]

    sudoku = Sudoku(puzzle)

    candidates = get_candidates(sudoku, 0, 2)

    assert candidates == {1, 2, 4}


def test_filled_cell_has_no_candidates():
    puzzle = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 0],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]

    sudoku = Sudoku(puzzle)

    candidates = get_candidates(sudoku, 0, 0)

    assert candidates == set()


def test_candidates_for_another_empty_cell():
    puzzle = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 0],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]

    sudoku = Sudoku(puzzle)

    candidates = get_candidates(sudoku, 0, 3)

    assert candidates == {2, 6}


def test_get_all_candidates():
    puzzle = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 0],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]

    sudoku = Sudoku(puzzle)

    all_candidates = get_all_candidates(sudoku)

    assert (0, 2) in all_candidates
    assert all_candidates[(0, 2)] == {1, 2, 4}

    assert (0, 3) in all_candidates
    assert all_candidates[(0, 3)] == {2, 6}