# This is a sample Python script.
import Sudoku as sudo
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    number_grid = [[0, 0, 0,    0, 3, 0,    1, 7, 0],
                   [2, 1, 0,    7, 0, 0,    0, 6, 9],
                   [0, 5, 3,    0, 0, 0,    2, 0, 0],

                   [0, 3, 0,    9, 0, 0,    0, 0, 7],
                   [0, 4, 0,    0, 0, 7,    8, 0, 0],
                   [0, 0, 0,    6, 0, 3,    0, 0, 0],

                   [0, 6, 0,    0, 0, 0,    4, 5, 1],
                   [1, 8, 0,    0, 2, 0,    7, 0, 0],
                   [0, 7, 0,    5, 0, 0,    9, 0, 0]]
    sudoku = sudo.SudokuGrid(number_grid)
    sudoku.solve()
    sudoku.print()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
