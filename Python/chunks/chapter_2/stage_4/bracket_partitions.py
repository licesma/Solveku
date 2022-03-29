class Bracket:
    """..."""
    def define_partitions(self):
        self.partitions = [Partition(SudokuGrid.I, [cell.av_set for cell in bracket]) for bracket in self.all]

    def inverse_av_set(self, bracket):
         raw_av_sets = [{i for i in SudokuGrid.I if bracket[i].av_set is not None and omega in bracket[i].av_set} for omega in
         SudokuGrid.Omega]
         return [av_set if 1 <= len(av_set) else None for av_set in raw_av_sets]

    def define_inverse_partitions(self):
        self.inverse_partitions = [Partition(SudokuGrid.Omega, self.inverse_av_set(bracket) ) for bracket in self.all]


class SudokuGrid:
    """..."""
    def define_bracket_partitions(self):
        self.brackets.define_partitions()
        self.brackets.define_inverse_partitions()