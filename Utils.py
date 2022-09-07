import math


def print_grid(sudoku):
    sqrt = int(math.sqrt(sudoku.n))
    for row in sudoku.I:
        for col in sudoku.I:
            print(sudoku.grid[row][col].value, end=" ")
            if col % sqrt == sqrt-1:
                print("", end=" ")
        print("")
        if row % sqrt == sqrt-1:
            print("")

def print_av_set(sudoku):
    for i in sudoku.I:
        print("Row ", i)
        for j in sudoku.I:
            cell = sudoku.brackets.row[i][j]
            if cell.av_set is not None:
                print(j, ': ', cell.av_set)
            else:
                print("{}")
        print("_____________")

def print_data(stage_list, total_backtracks):
        return {'stage_one': stage_list.count('Stage 1'),
                'stage_two': stage_list.count('Stage 2'),
                'stage_three': stage_list.count('Stage 3'),
                'stage_four': stage_list.count('Stage 4'),
                'stage_five': stage_list.count('Stage 5'),
                'backtrack_prune': stage_list.count('Backtrack prune'),
                'backtrack': stage_list.count('Backtrack'),
                'total_backtracks': total_backtracks}