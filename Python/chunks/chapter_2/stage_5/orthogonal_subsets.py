class SudokuGrid:
    """..."""
    def define_orthogonal_partitions(self):
        self.brackets.define_orthogonal_partitions()

    def prune_orthogonal(self, target_brackets, source_indexes, omega):
        for bracket in target_brackets:
            for index in SudokuGrid.I:
                if index not in source_indexes:
                    bracket[index].av_set_remove(omega)

    def find_orthogonal_subset(self, source_partitions, target_brackets, m):
        for omega, partition in source_partitions.items():
            sub_partition = partition.get_sub_partition(m)
            if sub_partition is not None:
                source_indexes, target_indexes = sub_partition
                target_brackets = [target_brackets[index] for index in target_indexes]
                self.prune_orthogonal(target_brackets, source_indexes, omega)

    def stage_five(self, m):
        self.find_orthogonal_subset(self.brackets.orthogonal_row_partition, self.brackets.col, m)
        self.find_orthogonal_subset(self.brackets.orthogonal_col_partitional, self.brackets.row,m)
