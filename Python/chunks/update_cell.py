class SudokuGrid:
    """..."""

    def update_neighbors_available_set(self, row, col, num):
        for it in self.I:
            self.brackets.row[row][it].av_set_remove(num)
            self.brackets.col[col][it].av_set_remove(num)
            self.brackets.box[self.box_of(row, col)][it].av_set_remove(num)

    def update_cell(self, row, col, num):
        self.grid[row][col].value = num
        self.grid[row][col].av_set = None
        if num in self.brackets.rowImage[row] or num in self.brackets.colImage[col] or num in self.brackets.boxImage[
            self.box_of(row, col)]:
            raise Exception("Group constraint violated")
        self.brackets.rowImage[row].add(num)
        self.brackets.colImage[col].add(num)
        self.brackets.boxImage[self.box_of(row, col)].add(num)
        self.update_neighbors_available_set(row, col, num)