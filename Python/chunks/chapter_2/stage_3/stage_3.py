class SudokuGrid:
    """..."""
    def stage_three(self):
        row_intersections = self.find_intersection(self.brackets.box, self.root_div, box_type, row_type)
        col_intersections = self.find_intersection(self.brackets.box, self.root_mod, box_type, col_type)
        box_r_intersections = self.find_intersection(self.brackets.row, self.root_div, row_type, box_type)
        box_c_intersections = self.find_in2tersection(self.brackets.col, self.root_div, col_type, box_type)