class SudokuGrid:
    """..."""
    def define_available_sets(self):
        for row in self.I:
            for col in self.I:
                cell = self.grid[row][col]
                if not cell.has_value():
                    for val in self.Omega:
                        if val in self.brackets.rowImage[row] or val in self.brackets.colImage[col] or val in self.brackets.boxImage[self.box_of(row, col)]:
                            cell.av_set.remove(val)

    def __init__(self, number_grid):
        """..."""
        self.define_available_sets()