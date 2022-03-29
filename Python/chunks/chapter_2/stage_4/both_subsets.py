class SudokuGrid:
    """..."""
    def find_naked_subset(self, m):
        subset_result = self.find_subset(self.brackets.partitions, m)
        if subset_result is not None:
            index, sub_partition = subset_result
            naked_indexes, naked_values = sub_partition
            bracket = self.brackets.all[index]
            self.prune_cells([bracket[i] for i in SudokuGrid.I if i not in naked_indexes], naked_values)

    def find_hidden_subset(self, m):
        subset_result = self.find_subset(self.brackets.inverse_partitions, m)
        if subset_result is not None:
            index, sub_partition = subset_result
            hidden_values, hidden_indexes = sub_partition
            bracket = self.brackets.all[index]
            self.prune_cells([bracket[i] for i in hidden_indexes],
                             [omega for omega in SudokuGrid.Omega if omega not in hidden_values])

    def stage_four(self,m):
        self.find_naked_subset(m)
        self.find_hidden_subset(m)
