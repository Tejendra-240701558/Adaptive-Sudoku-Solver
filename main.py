from src.sudoku import Sudoku


def main():
    puzzle = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],

        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],

        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]

    sudoku = Sudoku(puzzle)

    print("Sudoku:")
    sudoku.display()

    print("\nNumber of empty cells:")
    print(sudoku.empty_count())

    print("\nFirst empty cell:")
    print(sudoku.empty_cells()[0])

    print("\nValue at row 1, column 1:")
    print(sudoku.get(0, 0))

    print("\nSetting row 1, column 3 to 4...")
    sudoku.set(0, 2, 4)

    print("\nUpdated Sudoku:")
    sudoku.display()


if __name__ == "__main__":
    main()