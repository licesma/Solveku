
class Bracket:
    def get_image(self, index):
        res = set()
        bracket = self.all[index]
        for cell in bracket:
            if cell.has_value():
                if cell.value in res:
                    raise Exception("Group constraint violated")
                else:
                    res.add(cell.value)
        return res

    def __init__(self, sudoku):
        self.row = [sudoku.grid[i] for i in range(sudoku.n)]
        self.col = [[sudoku.grid[j][i] for j in range(sudoku.n)] for i in range(sudoku.n)]
        self.box = [sudoku.box_cells(i) for i in range(sudoku.n)]
        self.all = [self.row[i] if i < sudoku.n else self.col[i - sudoku.n] if i < 2*sudoku.n else self.box[i - 2*sudoku.n] for i in range(3*sudoku.n)]
        self.all_images = [set() for i in range(3 * sudoku.n)]
        self.rowImage = [self.all_images[i] for i in range(sudoku.n)]
        self.colImage = [self.all_images[i] for i in range(sudoku.n, 2 * sudoku.n)]
        self.boxImage = [self.all_images[i] for i in range(2 * sudoku.n, 3 * sudoku.n)]
        for i in sudoku.I:
            self.rowImage[i] = self.get_image(i)
            self.colImage[i] = self.get_image(sudoku.n + i)
            self.boxImage[i] = self.get_image(2*sudoku.n + i)