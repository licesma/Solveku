class SudokuCell:
    """..."""
    def av_set_remove(self, value):
        if not self.has_value() and (value in self.av_set):
            self.av_set.remove(value)