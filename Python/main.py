# This is a sample Python script.
from Utils import print_grid, print_av_set
import Sudoku as sudo
import timeit

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    number_grid = [[0, 0, 0,    0, 0, 6,    9, 0, 0],
                   [5, 1, 0,    7, 2, 0,    0, 0, 0],
                   [0, 0, 3,    0, 0, 0,    0, 2, 0],

                   [0, 0, 0,    0, 7, 1,    0, 0, 0],
                   [1, 7, 4,    0, 0, 9,    5, 0, 0],
                   [0, 0, 2,    0, 4, 0,    0, 0, 0],

                   [0, 9, 0,    0, 0, 0,    6, 5, 0],
                   [0, 0, 8,    0, 0, 0,    0, 3, 2],
                   [3, 0, 0,    0, 5, 0,    0, 0, 0]]
    start = timeit.default_timer()
    sudoku = sudo.SudokuGrid(number_grid)
    sudoku.solve()
    stop = timeit.default_timer()
    print((stop-start)*1000)
    print(sudoku.data())
    print(sudoku)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
