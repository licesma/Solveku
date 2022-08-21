# This is a sample Python script.
import Sudoku as sudo
import timeit
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.





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
    #sudoku.print()
    #sudoku.find_backtracking_candidate()
    sudoku.solve()
    stop = timeit.default_timer()
    print((stop-start)*1000)
    print(sudoku.data())


    for i in range(len(sudoku.stage_list)):
        print(i,':',sudoku.stage_list[i])
   # print(sudoku.brackets.inverse_partitions[22].get_sub_partition(2))
    sudoku.print()
    #sudoku.print_av_set()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
