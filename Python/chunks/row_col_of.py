class SudokuGrid:
    """..."""
    @staticmethod
    def row_of(box, cell):
        root = int(math.sqrt(SudokuGrid.n))
        return root*int(box/root) + int(cell/root);

    @staticmethod
    def col_of(box, cell):
        root = int(math.sqrt(SudokuGrid.n))
        return root*int(box%root) + int(cell%root)