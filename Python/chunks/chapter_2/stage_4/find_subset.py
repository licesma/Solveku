class SudokuGrid:
    """..."""
    def find_subset(self, partitions, m):
        for index in range(len(partitions)):
            partition = partitions[index]
            sub_partition = partition.get_sub_partition(m)
            if sub_partition is not None:
                return [index, sub_partition]
        return None