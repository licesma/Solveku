
class Bracket:
    def row_of_box(self, box_index, cell_index):
        root = int(math.sqrt(SudokuGrid.n))
        return root*int(box_index/root) + int(cell_index/root)

    def get_row(self, bracket_index, cell_index):
        if bracket_index < SudokuGrid.n:
            return bracket_index
        elif bracket_index < 2*SudokuGrid.n:
            return cell_index
        else:
            return self.row_of_box(bracket_index - 2*SudokuGrid.n, cell_index)

    def col_of_box(self, box_index, cell_index):
        root = int(math.sqrt(SudokuGrid.n))
        return root*(box_index%root) + (cell_index%root)

    def get_col(self, bracket_index, cell_index):
        if bracket_index < SudokuGrid.n:
            return cell_index
        elif bracket_index < 2*SudokuGrid.n:
            return bracket_index - SudokuGrid.n
        else:
            return self.col_of_box(bracket_index - 2*SudokuGrid.n, cell_index)
    """..."""