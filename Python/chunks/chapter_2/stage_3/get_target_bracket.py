class SudokuGrid:
    """"..."""
    def get_target_bracket(self, root_index, target_index, root_type, target_type):
        if root_type == row_type:
            return self.brackets.box[self.box_of(root_index, math.sqrt(self.n) * target_index)]
        elif root_type == col_type:
            return self.brackets.box[self.box_of(math.sqrt(self.n) * target_index, root_index)]
        else:
            if target_type == row_type:
                return self.brackets.row[self.brackets.row_of_box(root_index, math.sqrt(self.n) * target_index)]
            else:
                return self.brackets.col[self.brackets.col_of_box(root_index, target_index)]