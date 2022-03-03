class SudokuGrid:
    n = 9
    I = [i for i in range(n)]
    Omega = [i for i in range(1,n+1)]

    def box_of(self, row, col):
        return 3 * int(row / 3) + int(col / 3)

    def box_cells(self, index):
        root = int(math.sqrt(self.n))
        start_row = root * int(index / root)
        start_col = root * int(index % root)
        return [self.grid[start_row + i][start_col + j] for i in range(root) for j in range(root)]

    def __init__(self, number_grid):
        self.grid = [[SudokuCell(num, True) if num != 0 else SudokuCell() for num in row] for row in number_grid]
        for row in self.I:
            for col in self.I:
                cell = self.grid[row][col]
                if not cell.has_value():
                    for val in self.Omega:
                        cell.av_set.add(val)