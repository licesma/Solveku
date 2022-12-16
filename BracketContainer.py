import math
from Cover import Cover


class BracketContainer:
    def __init__(self, sudoku):
        self.covers = None
        self.inverse_covers = None
        self.n = sudoku.n
        self.I = sudoku.I
        self.Omega = sudoku.Omega
        self.row = [sudoku.grid[i] for i in range(sudoku.n)]
        self.col = [[sudoku.grid[j][i] for j in range(sudoku.n)] for i in range(sudoku.n)]
        self.box = [sudoku.box_cells(i) for i in range(sudoku.n)]
        self.all = [
            self.row[i] if i < sudoku.n else self.col[i - sudoku.n] if i < 2 * sudoku.n else self.box[i - 2 * sudoku.n]
            for i in range(3 * sudoku.n)]
        self.all_images = [None for _ in range(3 * sudoku.n)]
        self.row_image = [self.all_images[i] for i in range(sudoku.n)]
        self.col_image = [self.all_images[i] for i in range(sudoku.n, 2 * sudoku.n)]
        self.box_image = [self.all_images[i] for i in range(2 * sudoku.n, 3 * sudoku.n)]
        self.fill_images()

    def fill_images(self):
        for i in self.I:
            self.row_image[i] = self.get_image(i)
            self.col_image[i] = self.get_image(self.n + i)
            self.box_image[i] = self.get_image(2 * self.n + i)
            self.all_images[i] = self.row_image[i]
            self.all_images[self.n + i] = self.col_image[i]
            self.all_images[2 * self.n + i] = self.box_image[i]

    def row_of_box(self, box_index, cell_index):
        root = int(math.sqrt(self.n))
        return root * int(box_index / root) + int(cell_index / root)

    def get_row(self, bracket_index, cell_index):
        if bracket_index < self.n:
            return bracket_index
        elif bracket_index < 2 * self.n:
            return cell_index
        else:
            return self.row_of_box(bracket_index - 2 * self.n, cell_index)

    def col_of_box(self, box_index, cell_index):
        root = int(math.sqrt(self.n))
        return root * (box_index % root) + (cell_index % root)

    def get_col(self, bracket_index, cell_index):
        if bracket_index < self.n:
            return cell_index
        elif bracket_index < 2 * self.n:
            return bracket_index - self.n
        else:
            return self.col_of_box(bracket_index - 2 * self.n, cell_index)

    def has_every_candidate(self, bracket_index, map):
        for omega in self.Omega:
            if omega not in self.all_images[bracket_index] and omega not in map.keys():
                raise Exception("Candidate missing in bracket")

    def define_covers(self):
        self.covers = [Cover(self.I,
                                 [cell.av_set if cell.av_set is not None and 2 <= len(cell.av_set) else None for cell in
                                  bracket]) for bracket in self.all]

    def inverse_av_set(self, bracket):
        raw_av_sets = [{i for i in self.I if bracket[i].av_set is not None and omega in bracket[i].av_set} for omega in
                       self.Omega]
        return [av_set if 1 <= len(av_set) else None for av_set in raw_av_sets]

    def define_inverse_covers(self):
        self.inverse_covers = [Cover(self.Omega, self.inverse_av_set(bracket)) for bracket in self.all]

    def orthogonal_bracket_function(self, bracket, omega):
        res = {cell_index for cell_index in self.I if
               bracket[cell_index].av_set is not None and omega in bracket[cell_index].av_set}
        return res if 2 <= len(res) else None

    def define_orthogonal_covers(self):
        self.orthogonal_row_cover = {
            omega: Cover(self.I, [self.orthogonal_bracket_function(bracket, omega) for bracket in self.row])
            for omega in self.Omega}
        self.orthogonal_col_cover = {
            omega: Cover(self.I, [self.orthogonal_bracket_function(bracket, omega) for bracket in self.col])
            for omega in self.Omega}

    def get_image(self, index):
        res = set()
        bracket = self.all[index]
        for cell in bracket:
            if cell.has_value():
                if cell.value in res:
                    raise Exception("Bracket constraint violated")
                else:
                    res.add(cell.value)
        return res
