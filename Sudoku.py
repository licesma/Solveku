import math
from Cell import Cell
from BracketContainer import BracketContainer
from Constants import *


class SudokuGrid:

    # __________________________________________________________________________________________________________________
    # ____________________________________________GENERAL METHODS_______________________________________________________
    # __________________________________________________________________________________________________________________
    def __init__(self,n, number_grid):
        self.stage_list = None
        self.n = n
        self.I = [i for i in range(n)]
        self.Omega = [i for i in range(1, n + 1)]
        self.total_backtracks = 0
        if isinstance(number_grid, SudokuGrid):
            self.grid = [[number_grid.grid[row][col].copy() for col in self.I] for row in self.I]
            self.brackets = BracketContainer(self)
        else:
            self.grid = [[Cell(num, True) if num != 0 else Cell() for num in row] for row in number_grid]
            for row in self.I:
                for col in self.I:
                    cell = self.grid[row][col]
                    if not cell.has_value():
                        for val in self.Omega:
                            cell.av_set.add(val)
            self.brackets = BracketContainer(self)
            self.define_available_sets()


    def define_available_sets(self):
        for row in self.I:
            for col in self.I:
                cell = self.grid[row][col]
                if not cell.has_value():
                    for val in self.Omega:
                        if val in self.brackets.row_image[row] or val in self.brackets.col_image[col] or val in self.brackets.box_image[self.box_of(row, col)]:
                            cell.av_set.remove(val)

    def box_of(self, row, col):
        root = int(math.sqrt(self.n))
        return root*int(row/root) + int(col/root)

    def box_cells(self, index):
        root = int(math.sqrt(self.n))
        start_row = root * int(index / root)
        start_col = root * int(index % root)
        return [self.grid[start_row + i][start_col + j] for i in range(root) for j in range(root)]

    # __________________________________________________________________________________________________________________
    # ________________________________________ CELL  MANAGEMENT_________________________________________________________
    # __________________________________________________________________________________________________________________

    def update_neighbors_available_set(self, row, col, num):
        for it in self.I:
            self.brackets.row[row][it].av_set_remove(num)
            self.brackets.col[col][it].av_set_remove(num)
            self.brackets.box[self.box_of(row,col)][it].av_set_remove(num)

    def update_cell(self, row, col, num):
        self.grid[row][col].value = num
        self.grid[row][col].av_set = None
        if num in self.brackets.row_image[row]\
                or num in self.brackets.col_image[col] \
                or num in self.brackets.box_image[self.box_of(row, col)]:
            raise Exception("Bracket constraint violated")
        self.brackets.row_image[row].add(num)
        self.brackets.col_image[col].add(num)
        self.brackets.box_image[self.box_of(row,col)].add(num)
        self.update_neighbors_available_set(row, col, num)

    @staticmethod
    def prune_cells(cells, values):
        for cell in cells:
            for omega in values:
                cell.av_set_remove(omega)

    # _______________________________________________________________________________________________________________
    # ____________________________________________STAGE ONE___________________________________________________________
    # ________________________________________________________________________________________________________________

    def stage_one(self):
        changes = False
        for row in self.I:
            for col in self.I:
                cell = self.grid[row][col]
                if not cell.has_value() and len(cell.av_set) == 1:
                    changes = True
                    for num in cell.av_set:
                        self.update_cell(row, col, num)
        return changes

    # _______________________________________________________________________________________________________________
    # ____________________________________________STAGE TWO___________________________________________________________
    # ________________________________________________________________________________________________________________

    def stage_two(self):
        changes = False
        for bracket_index in range(len(self.brackets.all)):
            bracket = self.brackets.all[bracket_index]
            candidate_map = {}
            for cell_index in self.I:
                cell = bracket[cell_index]
                if not cell.has_value():
                    for candidate in cell.av_set:
                        if candidate in candidate_map :
                            candidate_map[candidate] = -1
                        else:
                            candidate_map[candidate] = cell_index
            self.brackets.has_every_candidate(bracket_index, candidate_map)
            for candidate, cell_index in candidate_map.items():
                if 0 <= cell_index :
                    row = self.brackets.get_row(bracket_index, cell_index)
                    col = self.brackets.get_col(bracket_index, cell_index)
                    self.update_cell(row, col, candidate)
                    changes = True
        return changes

    # _______________________________________________________________________________________________________________
    # ____________________________________________STAGE THREE_________________________________________________________
    # ________________________________________________________________________________________________________________

    @staticmethod
    def root_division_split_function(n, index):
        return int(index/math.sqrt(n))

    @staticmethod
    def root_module_split_function(n, index):
        return int(index % math.sqrt(n))

    def get_target_bracket(self, root_index, target_index, root_type, target_type):
        if root_type == ROW_TYPE:
            return self.brackets.box[self.box_of(root_index, math.sqrt(self.n)*target_index)]
        elif root_type == COL_TYPE:
            return self.brackets.box[self.box_of(math.sqrt(self.n)*target_index, root_index)]
        else:
            if target_type == ROW_TYPE:
                return self.brackets.row[self.brackets.row_of_box(root_index, math.sqrt(self.n)*target_index)]
            else:
                return self.brackets.col[self.brackets.col_of_box(root_index, target_index)]

    @staticmethod
    def prune_bracket(self, target_bracket, intersection, intersection_value):
        res = False
        for cell in target_bracket:
            if cell not in intersection:
                if cell.av_set_remove(intersection_value):
                    res = True
        return res

    def find_intersection(self, root_brackets, split_function, root_type, target_type):
        changes = False
        target_map = {}
        intersection_map = {}
        for root_index in self.I:
            target_map.clear()
            intersection_map.clear()
            root = root_brackets[root_index]
            for cell_index in self.I:
                cell = root[cell_index]
                target_index = split_function(cell_index)
                if not cell.has_value():
                    for candidate in cell.av_set:
                        if not candidate in target_map:
                            target_map[candidate] = target_index
                            intersection_map[candidate] = {cell}
                        else:
                            if target_map[candidate] == target_index:
                                intersection_map[candidate].add(cell)
                            else:
                                intersection_map[candidate] = None
                                target_map[candidate] = -1

            for candidate, target_index in target_map.items():
                if target_index in self.I:
                    target_bracket = self.get_target_bracket(root_index, target_index, root_type, target_type)
                    prune_res = self.prune_bracket(target_bracket, intersection_map[candidate], candidate)
                    changes = changes or prune_res
        return changes

    def stage_three(self):
        def division_split(index):
            return self.root_division_split_function(self.n, index)

        def module_split(index):
            return self.root_module_split_function(self.n, index)

        row_intersections = self.find_intersection(self.brackets.box, division_split, BOX_TYPE, ROW_TYPE)
        col_intersections = self.find_intersection(self.brackets.box, module_split, BOX_TYPE, COL_TYPE)
        box_r_intersections = self.find_intersection(self.brackets.row, division_split, ROW_TYPE, BOX_TYPE)
        box_c_intersections = self.find_intersection(self.brackets.col, division_split, COL_TYPE, BOX_TYPE)
        return row_intersections or col_intersections or box_r_intersections or box_c_intersections

    # _______________________________________________________________________________________________________________
    # _____________________________________________STAGE FOUR_________________________________________________________
    # ________________________________________________________________________________________________________________

    def define_bracket_covers(self):
        self.brackets.define_covers()
        self.brackets.define_inverse_covers()

    # Shared method used for finding naked or hidden subsets.
    @staticmethod
    def find_internal_bracket_subset(self, covers, m):
        for index in range(len(covers)):
            cover = covers[index]
            sub_cover = cover.get_sub_cover(m)
            if sub_cover is not None:
                return [index, sub_cover]
        return None

    def find_naked_subset(self, m):
        subset_result = self.find_internal_bracket_subset(self.brackets.covers, m)
        if subset_result is not None:
            index, sub_cover = subset_result
            naked_indexes, naked_values = sub_cover
            bracket = self.brackets.all[index]
            self.prune_cells([bracket[i] for i in self.I if i not in naked_indexes], naked_values)
            return True
        return False

    def find_hidden_subset(self, m):
        subset_result = self.find_internal_bracket_subset(self.brackets.inverse_covers,m)
        if subset_result is not None:
            index, sub_cover = subset_result
            hidden_values, hidden_indexes = sub_cover
            bracket = self.brackets.all[index]
            self.prune_cells([bracket[i] for i in hidden_indexes],
                             [omega for omega in self.Omega if omega not in hidden_values])
            return True
        return False



    def stage_four(self,m):
        return self.find_naked_subset(m) or self.find_hidden_subset(m)

    # _______________________________________________________________________________________________________________
    # _____________________________________________STAGE FIVE_________________________________________________________
    # ________________________________________________________________________________________________________________
    def define_orthogonal_covers(self):
        self.brackets.define_orthogonal_covers()

    def prune_orthogonal(self, target_brackets, source_indexes, omega):
        for bracket in target_brackets:
            for index in self.I:
                if index not in source_indexes:
                    bracket[index].av_set_remove(omega)

    def find_orthogonal_subset(self, source_covers, target_brackets, m, source_str, normal_str):
        for omega, cover in source_covers.items():
            sub_cover = cover.get_sub_cover(m)
            if sub_cover is not None:
                source_indexes, target_indexes = sub_cover
                target_brackets = [target_brackets[index] for index in target_indexes]
                self.prune_orthogonal(target_brackets, source_indexes, omega)
                return True
        return False

    def stage_five(self, m):
        return self.find_orthogonal_subset(self.brackets.orthogonal_row_cover, self.brackets.col, m, 'rows', 'cols') \
               or self.find_orthogonal_subset(self.brackets.orthogonal_col_cover, self.brackets.row, m, 'cols', 'rows')

    # __________________________________________________________________________________________________________________
    # ______________________________________BACKTRACK & HEURISTIC_______________________________________________________
    # __________________________________________________________________________________________________________________
    @staticmethod
    def xor(condition_1, condition_2):
        return (condition_1 and not condition_2) or (not condition_1 and condition_2)

    @staticmethod
    def rate_bracket(self, main_cell, bracket, omega, rate_array):
        for cell in bracket:
            av_set = cell.av_set
            if cell != main_cell and av_set is not None and omega in av_set and 2 <= len(av_set):
                rate_array[len(av_set)-2] += 1

    def remove_repeated_cells(self, row, col, omega, rate_list):
        # Return indexes of the box of the cell in (row, col), without the intersection with row and col.
        root = math.sqrt(self.n)
        full_box = self.brackets.box[self.box_of(row,col)]
        repeated_cells = [full_box[index]
                          for index in self.I if self.xor(int(index/root) == row % root, index % root == col % root)]
        for cell in repeated_cells:
            if cell.av_set is not None and omega in cell.av_set and 2 <= len(cell.av_set):
                rate_list[len(cell.av_set)-2] -= 1

    def rate_cell_candidate(self, row, col, omega):
        cell = self.grid[row][col]
        rate_list = [0 for _ in self.I]
        rate_list[len(cell.av_set)-2] += 1
        self.rate_bracket(cell, self.brackets.row[row], omega, rate_list)
        self.rate_bracket(cell, self.brackets.col[col], omega, rate_list)
        self.rate_bracket(cell, self.brackets.box[self.box_of(row, col)], omega, rate_list)
        self.remove_repeated_cells(row, col, omega, rate_list)
        return rate_list

    @staticmethod
    def is_first_rate_smaller(rate_list_1, rate_list_2):
        for i in range(len(rate_list_1)):
            if rate_list_1[i] < rate_list_2[i] :
                return True
            elif rate_list_2[i] < rate_list_1[i] :
                return False
        return False

    def find_backtracking_candidate(self):
        res = [-1, -1, -1]
        max_rate = [0 for _ in self.I]
        for row in self.I:
            for col in self.I:
                av_set =  self.grid[row][col].av_set
                if av_set is not None:
                    for omega in av_set:
                        current_rate = self.rate_cell_candidate(row, col, omega)
                        if self.is_first_rate_smaller(max_rate, current_rate):
                            max_rate = current_rate
                            res = [row, col, omega]
        return res

    # __________________________________________________________________________________________________________________
    # ______________________________________BACKTRACK & HEURISTIC_______________________________________________________
    # __________________________________________________________________________________________________________________

    def is_finished(self):
        for image in self.brackets.row_image:
            if len(image) != 9:
                return False
        return True

    def solve(self, active_stages=ALL_STAGES_ARRAY):
        self.stage_list = []
        while not self.is_finished():
            if STAGE_ONE_INDEX in active_stages and self.stage_one():
                self.stage_list.append(STAGE_ONE_LABEL)
            elif STAGE_TWO_INDEX in active_stages and self.stage_two():
                self.stage_list.append(STAGE_TWO_LABEL)
            elif STAGE_THREE_INDEX in active_stages and self.stage_three():
                self.stage_list.append(STAGE_THREE_LABEL)
            else:
                half = int(self.n/2)
                self.define_bracket_covers()
                self.define_orthogonal_covers()
                subset_found = False
                for m in range(2,half+1):
                    if STAGE_FOUR_INDEX in self.stage_four(m):
                        subset_found = True
                        self.stage_list.append(STAGE_FOUR_LABEL)
                        break
                    if STAGE_FIVE_INDEX in active_stages and self.stage_five(m):
                        subset_found = True
                        self.stage_list.append(STAGE_FIVE_LABEL)
                        break
                if not subset_found:
                    backtrack_grid = self(self)
                    row, col, omega = self.find_backtracking_candidate()
                    backtrack_grid.update_cell(row, col, omega)
                    self.total_backtracks += 1
                    try:
                        if backtrack_grid.solve():
                            self.stage_list.append(BACKTRACK_LABEL)
                            self.stage_list = self.stage_list + backtrack_grid.stage_list
                            self.grid = backtrack_grid.grid
                            self.total_backtracks += backtrack_grid.total_backtracks
                            return True
                        else:
                            self.prune_cells([self.grid[row][col]], [omega])
                    except:
                        self.stage_list.append(BACKTRACK_PRUNE_LABEL)
                        self.prune_cells([self.grid[row][col]], [omega])
                    self.total_backtracks += backtrack_grid.total_backtracks
        return self.is_finished()
