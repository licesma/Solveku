class SudokuGrid:
    """..."""
    def stage_one(self):
        for row in self.I:
            for col in self.I:
                cell = self.grid[row][col]
                if not cell.has_value() and len(cell.av_set) == 1:
                    for num in cell.av_set:
                        self.update_cell(row, col, num)