# This is a sample Python script.
import Sudoku as sudo
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    number_grid = [[0, 0, 0,    0, 0, 0,    0, 0, 0],
                   [0, 7, 0,    0, 3, 0,    9, 2, 0],
                   [0, 1, 9,    0, 2, 5,    6, 3, 0],

                   [0, 0, 4,    0, 0, 0,    2, 1, 0],
                   [0, 0, 0,    0, 0, 0,    0, 0, 0],
                   [0, 5, 7,    0, 9, 0,    4, 6, 0],

                   [0, 9, 5,    1, 4, 0,    3, 7, 0],
                   [7, 0, 0,    0, 0, 0,    0, 4, 0],
                   [0, 4, 2,    3, 6, 7,    5, 9, 0]]

    sudoku = sudo.SudokuGrid(number_grid)
    sudoku.solve()
    #sudoku.print()
    #sudoku.print_av_set()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
