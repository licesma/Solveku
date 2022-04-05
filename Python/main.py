# This is a sample Python script.
import Sudoku as sudo
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    number_grid = [[0, 0, 0,    0, 1, 0,    0, 0, 0],
                   [0, 6, 0,    0, 0, 0,    0, 9, 0],
                   [0, 0, 8,    2, 4, 0,    0, 0, 6],

                   [4, 0, 0,    5, 2, 0,    0, 3, 0],
                   [0, 0, 0,    0, 0, 1,    0, 0, 2],
                   [0, 0, 5,    0, 0, 9,    0, 0, 0],

                   [0, 0, 4,    8, 6, 0,    0, 0, 9],
                   [0, 0, 0,    0, 0, 5,    0, 0, 0],
                   [3, 0, 0,    0, 0, 0,    7, 0, 0]]

    sudoku = sudo.SudokuGrid(number_grid)
    #sudoku.print()
    #sudoku.find_backtracking_candidate()
    sudoku.solve()
    for i in range(len(sudoku.stage_list)):
        print(i,':',sudoku.stage_list[i])
    print(sudoku.brackets.inverse_partitions[22].get_sub_partition(2))
    sudoku.print()
    #sudoku.print_av_set()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
