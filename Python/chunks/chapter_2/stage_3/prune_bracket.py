class SudokuGrid:
    """..."""
    def prune_bracket(self, target_bracket, intersection, intersection_value):
        res = False
        for cell in target_bracket:
            if cell not in intersection:
                if cell.av_set_remove(intersection_value):
                    res = True
        return res