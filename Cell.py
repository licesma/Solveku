UNSOLVABLE_LABEL = "Unsolvable puzzle"


class Cell:
    def __init__(self, value=0, fixed=False):
        # fixed: cell had a value since the beginning of the puzzle.
        self.value = value
        self.fixed = fixed
        self.av_set = None
        if not fixed:
            self.av_set = set()

    # Returns if the cell has an associated value.
    def has_value(self):
        return self.value != 0

    # Safe checks and removes a value from an available sets.
    # Also checks unsolvable puzzles.
    def av_set_remove(self, value):
        if not self.has_value() and (value in self.av_set):
            self.av_set.remove(value)
            if len(self.av_set) == 0:
                raise Exception(UNSOLVABLE_LABEL)
            return True
        return False

    # Return a deep copy of the cell.
    def deep_copy(self):
        deep_copy = Cell()
        deep_copy.value = self.value
        if self.av_set is not None:
            deep_copy.av_set = self.av_set.copy()
        deep_copy.fixed = self.fixed
        return deep_copy
