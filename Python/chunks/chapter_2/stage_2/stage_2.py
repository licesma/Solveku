class SudokuGrid:
    def stage_two(self):
        for bracket_index in range(len(self.brackets.all)):
            bracket = self.brackets.all[bracket_index]
            candidate_map = {}
            for cell_index in SudokuGrid.I:
                cell = bracket[cell_index]
                if not cell.has_value():
                    for candidate in cell.av_set:
                        if candidate in candidate_map:
                            candidate_map[candidate] = -1
                        else:
                            candidate_map[candidate] = cell_index
            for candidate, cell_index in candidate_map.items():
                if 0 <= cell_index:
                    row = self.brackets.get_row(bracket_index, cell_index)
                    col = self.brackets.get_col(bracket_index, cell_index)
                    self.update_cell(row, col, candidate)