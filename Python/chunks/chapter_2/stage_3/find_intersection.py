class SudokuGrid:
    """..."""
    @staticmethod
    def root_div(index):
        return int(index/math.sqrt(SudokuGrid.n))

    @staticmethod
    def root_mod(index):
        return int(index%math.sqrt(SudokuGrid.n))

    def find_intersection(self, root_brackets, split_function, root_type, target_type):
        target_map = {}
        intersection_map = {}
        for root_index in self.I:
            target_map.clear()
            intersection_map.clear()
            root = root_brackets[root_index]
            for cell_index in self.I:
                cell = root[cell_index]
                target_index = split_function(cell_index)
                if not cell.has_value():
                    for candidate in cell.av_set:
                        if not candidate in target_map:
                            target_map[candidate] = target_index
                            intersection_map[candidate] = {cell}
                        else:
                            if target_map[candidate] == target_index:
                                intersection_map[candidate].add(cell)
                            else:
                                intersection_map[candidate] = None
                                target_map[candidate] = -1
            for candidate, target_index in target_map.items():
                if target_index in SudokuGrid.I:
                    target_bracket = self.get_target_bracket(root_index, target_index, root_type, target_type)
                    self.prune_bracket(target_bracket, intersection_map[candidate], candidate)
