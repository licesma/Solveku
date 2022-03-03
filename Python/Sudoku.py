import math
class SudokuCell:
    n = 9
    def __init__(self, value=0, fixed=False):
        self.value = value
        self.fixed = fixed
        self.av_set = None
        if not fixed:
            self.av_set = set()

    def has_value(self):
        return self.value != 0

    def av_set_remove(self, value):
        if not self.has_value() and (value in self.av_set):
            self.av_set.remove(value)


class Bracket:

    @staticmethod
    def row_of_box(box_index, cell_index):
        root = int(math.sqrt(SudokuGrid.n))
        return root*int(box_index/root) + int(cell_index/root)

    def get_row(self, bracket_index, cell_index):
        if bracket_index < SudokuGrid.n:
            return bracket_index
        elif bracket_index < 2*SudokuGrid.n:
            return cell_index
        else:
            return self.row_of_box(bracket_index - 2*SudokuGrid.n, cell_index)

    @staticmethod
    def col_of_box(box_index, cell_index):
        root = int(math.sqrt(SudokuGrid.n))
        return root*(box_index%root) + (cell_index%root)

    def get_col(self, bracket_index, cell_index):
        if bracket_index < SudokuGrid.n:
            return cell_index
        elif bracket_index < 2*SudokuGrid.n:
            return bracket_index - SudokuGrid.n
        else:
            return self.col_of_box(bracket_index - 2*SudokuGrid.n, cell_index)

    def get_image(self, index):
        res = set()
        bracket = self.all[index]
        for cell in bracket:
            if cell.has_value():
                if cell.value in res:
                    raise Exception("Group constraint violated")
                else:
                    res.add(cell.value)
        return res

    def __init__(self, sudoku):
        self.row = [sudoku.grid[i] for i in range(sudoku.n)]
        self.col = [[sudoku.grid[j][i] for j in range(sudoku.n)] for i in range(sudoku.n)]
        self.box = [sudoku.box_cells(i) for i in range(sudoku.n)]
        self.all = [self.row[i] if i < sudoku.n else self.col[i - sudoku.n] if i < 2*sudoku.n else self.box[i - 2*sudoku.n] for i in range(3*sudoku.n)]
        self.all_images = [set() for _ in range(3 * sudoku.n)]
        self.rowImage = [self.all_images[i] for i in range(sudoku.n)]
        self.colImage = [self.all_images[i] for i in range(sudoku.n, 2 * sudoku.n)]
        self.boxImage = [self.all_images[i] for i in range(2 * sudoku.n, 3 * sudoku.n)]
        for i in sudoku.I:
            self.rowImage[i] = self.get_image(i)
            self.colImage[i] = self.get_image(sudoku.n + i)
            self.boxImage[i] = self.get_image(2*sudoku.n + i)

class SudokuGrid:
    n = 9
    I = [i for i in range(n)]
    Omega = [i for i in range(1,n+1)]

    @staticmethod
    def box_of(row, col):
        return 3 * int(row / 3) + int(col / 3)

    def box_cells(self, index):
        root = int(math.sqrt(self.n))
        start_row = root * int(index / root)
        start_col = root * int(index % root)
        return [self.grid[start_row + i][start_col + j] for i in range(root) for j in range(root)]

    def define_available_sets(self):
        for row in self.I:
            for col in self.I:
                cell = self.grid[row][col]
                if not cell.has_value():
                    for val in self.Omega:
                        if val in self.brackets.rowImage[row] or val in self.brackets.colImage[col] or val in self.brackets.boxImage[self.box_of(row, col)]:
                            cell.av_set.remove(val)

    def update_neighbors_available_set(self, row, col, num):
        for it in self.I:
            self.brackets.row[row][it].av_set_remove(num)
            self.brackets.col[col][it].av_set_remove(num)
            self.brackets.box[self.box_of(row,col)][it].av_set_remove(num)

    def update_cell(self, row, col, num):
        self.grid[row][col].value = num
        self.grid[row][col].av_set = None
        if num in self.brackets.rowImage[row] or num in self.brackets.colImage[col] or num in self.brackets.boxImage[self.box_of(row,col)]:
            raise Exception("Group constraint violated")
        self.brackets.rowImage[row].add(num)
        self.brackets.colImage[col].add(num)
        self.brackets.boxImage[self.box_of(row,col)].add(num)
        self.update_neighbors_available_set(row, col, num)

    def stage_one(self):
        changes = False
        for row in self.I:
            for col in self.I:
                cell = self.grid[row][col]
                if not cell.has_value() and len(cell.av_set) == 1:
                    changes = True
                    for num in cell.av_set:
                        self.update_cell(row, col, num)
        if changes:
            self.stage_one()
        else:
            self.stage_two()

    def stage_two(self):
        changes = False
        for bracket_index in range(len(self.brackets.all)):
            bracket = self.brackets.all[bracket_index]
            candidate_map = {}
            for cell_index in SudokuGrid.I:
                cell = bracket[cell_index]
                if not cell.has_value():
                    for candidate in cell.av_set:
                        if candidate in candidate_map :
                            candidate_map[candidate] = -1
                        else:
                            candidate_map[candidate] = cell_index
            for candidate, cell_index in candidate_map.items():
                if 0 <= cell_index :
                    row = self.brackets.get_row(bracket_index, cell_index)
                    col = self.brackets.get_col(bracket_index, cell_index)
                    self.update_cell(row, col, candidate)
                    changes = True
        if changes:
            self.stage_two()

    def solve(self):
        self.stage_two()

    def __init__(self, number_grid):
        self.grid = [[SudokuCell(num, True) if num != 0 else SudokuCell() for num in row] for row in number_grid]
        for row in self.I:
            for col in self.I:
                cell = self.grid[row][col]
                if not cell.has_value():
                    for val in self.Omega:
                        cell.av_set.add(val)
        self.brackets = Bracket(self)
        self.define_available_sets()

    def print(self):
        for row in self.I:
            for col in self.I:
                print(self.grid[row][col].value, end = " ")
                if col%3 == 2:
                    print("", end=" ")
            print("")
            if row%3 == 2:
                print("")
