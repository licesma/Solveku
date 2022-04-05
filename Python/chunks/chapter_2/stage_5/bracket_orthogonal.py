class Bracket:
    """..."""
    def orthogonal_bracket_function(self, bracket, omega):
        res = {cell_index for cell_index in SudokuGrid.I if bracket[cell_index].av_set is not None and omega in bracket[cell_index].av_set}
        return res if res else None

    def define_orthogonal_partitions(self):
        self.orthogonal_row_partition = {
            omega: Partition(SudokuGrid.I, [self.orthogonal_bracket_function(bracket, omega) for bracket in self.row])
            for omega in SudokuGrid.Omega}
        self.orthogonal_col_partition = {
            omega: Partition(SudokuGrid.I, [self.orthogonal_bracket_function(bracket, omega) for bracket in self.col])
            for omega in SudokuGrid.Omega}