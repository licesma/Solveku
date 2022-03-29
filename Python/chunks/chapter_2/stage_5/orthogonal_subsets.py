class SudokuGrid:
    """..."""
    def define_orthogonal_partitions(self):
        self.brackets.define_orthogonal_partitions()

    def prune_orthogonal_difference(self, prune_brackets, skip_indexes, omega):
        for bracket in prune_brackets:
            for index in SudokuGrid.I:
                if index not in skip_indexes:
                    bracket[index].av_set_remove(omega)

    def find_orthogonal_subset(self, source_partitions, orthogonal_brackets, m, source_str, normal_str):
        for omega, partition in source_partitions.items():
            sub_partition = partition.get_sub_partition(m)
            if sub_partition is not None:
                skip_indexes, prune_indexes = sub_partition
                prune_brackets = [orthogonal_brackets[index] for index in prune_indexes]
                self.prune_orthogonal_difference(prune_brackets, skip_indexes, omega)
                print(source_str, skip_indexes, ' ', normal_str, prune_indexes, ' ', omega)
                return True
        return False

    def stage_five(self, m):
        return self.find_orthogonal_subset(self.brackets.orthogonal_row_partition, self.brackets.col, m, 'rows',
                                           'cols') or self.find_orthogonal_subset(
            self.brackets.orthogonal_col_partitional,
            self.brackets.row, m, 'cols', 'rows')
