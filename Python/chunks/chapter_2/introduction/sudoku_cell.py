
class SudokuCell:
    n = 9
    def __init__(self, value=0, fixed=False):
        self.value = value
        self.fixed = fixed
        self.av_set = None
        if not fixed:
            self.av_set = set()

    def has_value(self):
        return self.value != 0

    def av_set_remove(self, value):
        if not self.has_value() and (value in self.av_set):
            self.av_set.remove(value)
