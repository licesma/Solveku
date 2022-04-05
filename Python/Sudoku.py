import math
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
            if len(self.av_set) == 0:
                raise Exception("Unsolvable puzzle")
            return True
        return False

    def copy(self):
        copy = SudokuCell()
        copy.value = self.value
        if self.av_set is not None:
            copy.av_set = self.av_set.copy()
        copy.fixed = self.fixed
        return copy

row_type = "ROW"
col_type = "COL"
box_type = "BOX"
class Bracket:

    @staticmethod
    def row_of_box(box_index, cell_index):
        root = int(math.sqrt(SudokuGrid.n))
        return root*int(box_index/root) + int(cell_index/root)

    def get_row(self, bracket_index, cell_index):
        if bracket_index < SudokuGrid.n:
            return bracket_index
        elif bracket_index < 2*SudokuGrid.n:
            return cell_index
        else:
            return self.row_of_box(bracket_index - 2*SudokuGrid.n, cell_index)

    @staticmethod
    def col_of_box(box_index, cell_index):
        root = int(math.sqrt(SudokuGrid.n))
        return root*(box_index%root) + (cell_index%root)

    def get_col(self, bracket_index, cell_index):
        if bracket_index < SudokuGrid.n:
            return cell_index
        elif bracket_index < 2*SudokuGrid.n:
            return bracket_index - SudokuGrid.n
        else:
            return self.col_of_box(bracket_index - 2*SudokuGrid.n, cell_index)

    def has_every_candidate(self, bracket_index, map):
        for omega in SudokuGrid.Omega:
            if omega not in self.all_images[bracket_index] and omega not in map.keys():
                raise Exception("Candidate missing in bracket")
    def define_partitions(self):
        self.partitions = [Partition(SudokuGrid.I, [cell.av_set for cell in bracket]) for bracket in self.all]

    def inverse_av_set(self, bracket):
         raw_av_sets = [{i for i in SudokuGrid.I if bracket[i].av_set is not None and omega in bracket[i].av_set} for omega in
         SudokuGrid.Omega]
         return [av_set if 1 <= len(av_set) else None for av_set in raw_av_sets]

    def define_inverse_partitions(self):
        self.inverse_partitions = [Partition(SudokuGrid.Omega, self.inverse_av_set(bracket) ) for bracket in self.all]


    def orthogonal_bracket_function(self, bracket, omega):
        res = {cell_index for cell_index in SudokuGrid.I if bracket[cell_index].av_set is not None and omega in bracket[cell_index].av_set}
        return res if res else None

    def define_orthogonal_partitions(self):
        self.orthogonal_row_partition = {
            omega: Partition(SudokuGrid.I, [self.orthogonal_bracket_function(bracket, omega) for bracket in self.row])
            for omega in SudokuGrid.Omega}
        self.orthogonal_col_partition = {
            omega: Partition(SudokuGrid.I, [self.orthogonal_bracket_function(bracket, omega) for bracket in self.col])
            for omega in SudokuGrid.Omega}

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
        self.all_images = [None for _ in range(3 * sudoku.n)]
        self.row_image = [self.all_images[i] for i in range(sudoku.n)]
        self.col_image = [self.all_images[i] for i in range(sudoku.n, 2 * sudoku.n)]
        self.box_image = [self.all_images[i] for i in range(2 * sudoku.n, 3 * sudoku.n)]
        for i in sudoku.I:
            self.row_image[i] = self.get_image(i)
            self.col_image[i] = self.get_image(sudoku.n + i)
            self.box_image[i] = self.get_image(2*sudoku.n + i)
            self.all_images[i] = self.row_image[i]
            self.all_images[sudoku.n+i] = self.col_image[i]
            self.all_images[2*sudoku.n +i] = self.box_image[i]


class Partition:
    def __init__(self, domain, image):
        self.domain = [domain[i] for i in SudokuGrid.I]
        self.image = [image[i] for i in SudokuGrid.I]

    def clear(self):
        self.sub_indexes = set()
        self.sub_image = set()
        self.valid_indexes = [index for index in SudokuGrid.I if (self.image[index] is not None and len(self.image[index]) <= self.m)]


    def get_sub_partition(self, m):
        self.m = m
        self.clear()
        if self.find_sub_partition(m):
            return [[self.domain[i] for i in self.sub_indexes], self.sub_image]
        else:
            return None

    def is_prunable(self, current_image):
        for image in current_image:
            for index in SudokuGrid.I:
                if index not in self.sub_indexes and self.image[index] is not None and image in self.image[index]:
                    return True
        return False

    def find_pair(self):
        past_images = {}
        for index in self.valid_indexes:
            if index not in  self.sub_indexes:
                current_image = frozenset(self.image[index].union(self.sub_image))
                if len(current_image) == self.m and current_image in past_images.keys():

                    self.sub_indexes.add(past_images[current_image])
                    self.sub_indexes.add(index)
                    if self.is_prunable(current_image):
                        self.sub_image = current_image
                        return True
                    else:
                        self.sub_indexes.remove(past_images[current_image])
                        self.sub_indexes.remove(index)
                else:
                    past_images[current_image] = index
        return False

    def find_sub_partition(self, partition_size):
        if partition_size == 2:
            return self.find_pair()
        else:
            valid_indexes = self.valid_indexes.copy()
            for index in valid_indexes:
                if index not in self.sub_indexes:
                    image = self.image[index]
                    self.sub_indexes.add(index)
                    last_sub_image = self.sub_image.copy()
                    self.sub_image = self.sub_image.union(image)
                    if len(self.sub_image) <= self.m and self.find_sub_partition(partition_size-1):
                        return True
                    self.sub_indexes.remove(index)
                    self.sub_image = last_sub_image
                if partition_size == self.m:
                    self.valid_indexes.remove(index)

            return False

class SudokuGrid:
    n = 9
    I = [i for i in range(n)]
    Omega = [i for i in range(1,n+1)]

    # _______________________________________________________________________________________________________________
    #____________________________________________GENERAL METHODS___________________________________________________________
    #________________________________________________________________________________________________________________
    def __init__(self, number_grid):
        if isinstance(number_grid, SudokuGrid):
            self.grid = [[number_grid.grid[row][col].copy() for col in SudokuGrid.I] for row in SudokuGrid.I]
            self.brackets = Bracket(self)
        else:
            self.grid = [[SudokuCell(num, True) if num != 0 else SudokuCell() for num in row] for row in number_grid]
            for row in self.I:
                for col in self.I:
                    cell = self.grid[row][col]
                    if not cell.has_value():
                        for val in self.Omega:
                            cell.av_set.add(val)
            self.brackets = Bracket(self)
            self.define_available_sets()


    def define_available_sets(self):
        for row in self.I:
            for col in self.I:
                cell = self.grid[row][col]
                if not cell.has_value():
                    for val in self.Omega:
                        if val in self.brackets.row_image[row] or val in self.brackets.col_image[col] or val in self.brackets.box_image[self.box_of(row, col)]:
                            cell.av_set.remove(val)

    @staticmethod
    def box_of(row, col):
        root = int(math.sqrt(SudokuGrid.n))
        return root*int(row/root) + int(col/root)

    def box_cells(self, index):
        root = int(math.sqrt(self.n))
        start_row = root * int(index / root)
        start_col = root * int(index % root)
        return [self.grid[start_row + i][start_col + j] for i in range(root) for j in range(root)]

    def print(self):
        for row in self.I:
            for col in self.I:
                print(self.grid[row][col].value, end = " ")
                if col%3 == 2:
                    print("", end=" ")
            print("")
            if row%3 == 2:
                print("")

    def print_av_set(self):
        for i in self.I:
            print("Row ", i)
            for j in self.I:
                cell = self.brackets.row[i][j]
                if cell.av_set is not None:
                    print(j, ': ', cell.av_set)
                else:
                    print("{}")
            print("_____________")
    # _______________________________________________________________________________________________________________
    #__________________________________________UPDATE CELL___________________________________________________________
    #________________________________________________________________________________________________________________

    def update_neighbors_available_set(self, row, col, num):
        for it in self.I:
            self.brackets.row[row][it].av_set_remove(num)
            self.brackets.col[col][it].av_set_remove(num)
            self.brackets.box[self.box_of(row,col)][it].av_set_remove(num)

    def update_cell(self, row, col, num):
        self.grid[row][col].value = num
        self.grid[row][col].av_set = None
        if num in self.brackets.row_image[row] or num in self.brackets.col_image[col] or num in self.brackets.box_image[self.box_of(row,col)]:
            raise Exception("Bracket constraint violated")
        self.brackets.row_image[row].add(num)
        self.brackets.col_image[col].add(num)
        self.brackets.box_image[self.box_of(row,col)].add(num)
        self.update_neighbors_available_set(row, col, num)

    # _______________________________________________________________________________________________________________
    #____________________________________________STAGE ONE___________________________________________________________
    #________________________________________________________________________________________________________________

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
    #____________________________________________STAGE TWO___________________________________________________________
    #________________________________________________________________________________________________________________

    def stage_two(self):
        changes = False
        for bracket_index in range(len(self.brackets.all)):
            bracket = self.brackets.all[bracket_index]
            candidate_map = {}
            for cell_index in SudokuGrid.I:
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
    #____________________________________________STAGE THREE_________________________________________________________
    #________________________________________________________________________________________________________________

    @staticmethod
    def root_div(index):
        return int(index/math.sqrt(SudokuGrid.n))

    @staticmethod
    def root_mod(index):
        return int(index%math.sqrt(SudokuGrid.n))

    def get_target_bracket(self, root_index, target_index, root_type, target_type):
        if root_type == row_type:
            return self.brackets.box[self.box_of(root_index, math.sqrt(self.n)*target_index)]
        elif root_type == col_type:
            return self.brackets.box[self.box_of(math.sqrt(self.n)*target_index, root_index)]
        else:
            if target_type == row_type:
                return self.brackets.row[self.brackets.row_of_box(root_index, math.sqrt(self.n)*target_index)]
            else:
                return self.brackets.col[self.brackets.col_of_box(root_index, target_index)]

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
            condition =  root_type == box_type and target_type == col_type and root_index == 3 and False
            if condition:
                print('#############################################################################################')
                print(target_map)

            for candidate, target_index in target_map.items():
                if target_index in SudokuGrid.I:
                    target_bracket = self.get_target_bracket(root_index, target_index, root_type, target_type)
                    if condition:
                        print('candidate:', candidate)
                        print('target_bracket: ', [cell.value if cell.has_value() else cell.av_set for cell in target_bracket])
                        print('intersection_map', [cell.av_set for cell in intersection_map[candidate]])
                    prune_res = self.prune_bracket(target_bracket, intersection_map[candidate], candidate)
                    changes = changes or prune_res
                    if prune_res and False:
                        print('Stage 3: ', 'root:', root_type, root_index, ' target:', target_type, target_index, ' (', candidate, ')')
            if condition:
                condition = False
                print('#############################################################################################')
        return changes

    def stage_three(self):
        row_intersections = self.find_intersection(self.brackets.box, self.root_div, box_type, row_type)
        col_intersections = self.find_intersection(self.brackets.box, self.root_mod, box_type, col_type)
        box_r_intersections = self.find_intersection(self.brackets.row, self.root_div, row_type, box_type)
        box_c_intersections = self.find_intersection(self.brackets.col, self.root_div, col_type, box_type)
        return row_intersections or col_intersections or box_r_intersections or box_c_intersections
    # _______________________________________________________________________________________________________________
    # _____________________________________________STAGE FOUR_________________________________________________________
    # ________________________________________________________________________________________________________________

    def prune_cells(self, cells, values):
        for cell in cells:
            for omega in values:
                cell.av_set_remove(omega)


    def find_subset(self, partitions, m):
        for index in range(len(partitions)):
            partition = partitions[index]
            sub_partition = partition.get_sub_partition(m)
            if sub_partition is not None:
                return [index, sub_partition]
        return None

    def find_naked_subset(self, m):
        subset_result = self.find_subset(self.brackets.partitions, m)
        if subset_result is not None:
            index, sub_partition = subset_result
            naked_indexes, naked_values = sub_partition
            bracket = self.brackets.all[index]
            print("NAKED SUBSET FOUND, Bracket: ", index, ", -cells: ", naked_indexes, " -values: ", naked_values)
            self.prune_cells([bracket[i] for i in SudokuGrid.I if i not in naked_indexes], naked_values)
            return True
        return False

    def find_hidden_subset(self, m):
        subset_result = self.find_subset(self.brackets.inverse_partitions,m)
        if subset_result is not None:
            index, sub_partition = subset_result
            hidden_values, hidden_indexes = sub_partition
            bracket = self.brackets.all[index]
            print("HIDDEN SUBSET FOUND, Bracket: ", index, ", -cells: ", hidden_indexes, " -values: ", hidden_values)
            self.prune_cells([bracket[i] for i in hidden_indexes], [omega for omega in SudokuGrid.Omega if omega not in hidden_values])
            return True
        return False

    def define_bracket_partitions(self):
        self.brackets.define_partitions()
        self.brackets.define_inverse_partitions()

    def stage_four(self,m):
        return self.find_naked_subset(m) or self.find_hidden_subset(m)


    # _______________________________________________________________________________________________________________
    #_____________________________________________STAGE FIVE_________________________________________________________
    #________________________________________________________________________________________________________________
    def define_orthogonal_partitions(self):
        self.brackets.define_orthogonal_partitions()

    def prune_orthogonal(self, target_brackets, source_indexes, omega):
        for bracket in target_brackets:
            for index in SudokuGrid.I:
                if index not in source_indexes:
                    bracket[index].av_set_remove(omega)

    def find_orthogonal_subset(self, source_partitions, target_brackets, m, source_str, normal_str):
        for omega, partition in source_partitions.items():
            sub_partition = partition.get_sub_partition(m)
            if sub_partition is not None:
                source_indexes, target_indexes = sub_partition
                target_brackets = [target_brackets[index] for index in target_indexes]
                self.prune_orthogonal(target_brackets, source_indexes, omega)
                print(source_str, source_indexes, ' ', normal_str, target_indexes, ' ', omega)
                return True
        return False

    def stage_five(self, m):
        return self.find_orthogonal_subset(self.brackets.orthogonal_row_partition, self.brackets.col, m, 'rows', 'cols') or self.find_orthogonal_subset(self.brackets.orthogonal_col_partition, self.brackets.row, m, 'cols', 'rows')

    # _______________________________________________________________________________________________________________
    #___________________________________________BACKTRACKING_________________________________________________________
    #________________________________________________________________________________________________________________
    @staticmethod
    def xor(condition_1, condition_2):
        return (condition_1 and not condition_2) or (not condition_1 and condition_2)

    def substract_repeated_cells(self, row, col, omega, rate_list):
        # Return indexes of the box of the cell in (row, col), without the intersection with row and col.
        root = math.sqrt(self.n)
        full_box = self.brackets.box[self.box_of(row,col)]
        repeated_cells = [full_box[index] for index in self.I if self.xor(int(index/root) == row%root, index%root == col%root)]
        for cell in repeated_cells:
            if  cell.av_set is not None and omega in cell.av_set and 2 <= len(cell.av_set):
                rate_list[len(cell.av_set)-2] -= 1

    def rate_bracket(self, main_cell, bracket, omega, rate_array):
        for cell in bracket:
            av_set = cell.av_set
            if cell != main_cell and av_set is not None and omega in av_set and 2 <= len(av_set):
                rate_array[len(av_set)-2] += 1

    def rate_cell_candidate(self, row, col, omega):
        cell = self.grid[row][col]
        rate_list = [0 for _ in SudokuGrid.I]
        rate_list[len(cell.av_set)-2] += 1
        self.rate_bracket(cell, self.brackets.row[row], omega, rate_list)
        self.rate_bracket(cell, self.brackets.col[col], omega, rate_list)
        self.rate_bracket(cell, self.brackets.box[self.box_of(row,col)], omega, rate_list)
        self.substract_repeated_cells(row, col, omega, rate_list)
        return rate_list

    def first_is_smaller(self, rate_list_1, rate_list_2):
        for i in range(len(rate_list_1)):
            if rate_list_1[i] < rate_list_2[i] :
                return True
            elif rate_list_2[i] < rate_list_1[i] :
                return False
        return False
    def find_backtracking_candidate(self):
        res = [-1, -1, -1]
        max_rate = [0 for _ in SudokuGrid.I]
        for row in self.I:
            for col in self.I:
                av_set =  self.grid[row][col].av_set
                if av_set is not None:
                    for omega in av_set:
                        current_rate = self.rate_cell_candidate(row, col, omega)
                        if self.first_is_smaller(max_rate, current_rate):
                            max_rate = current_rate
                            res = [row, col, omega]
        return res

    def is_finished(self):
        for image in self.brackets.row_image:
            if len(image) != 9:
                return False
        return True

    def solve(self):
        self.stage_list = []
        while not self.is_finished():
            if self.stage_one():
                self.stage_list.append('Stage 1')
            elif self.stage_two():
                self.stage_list.append('Stage 2')
            elif self.stage_three():
                self.stage_list.append('Stage 3')
            else:
                half = int(self.n/2)
                self.define_bracket_partitions()
                self.define_orthogonal_partitions()
                subset_found = False
                for m in range(2,half+1):
                    if self.stage_four(m):
                        subset_found = True
                        self.stage_list.append('Stage 4')
                        break
                    if self.stage_five(m):
                        subset_found = True
                        self.stage_list.append('Stage 5')
                        break
                if  not subset_found:
                    backtrack_grid = SudokuGrid(self)
                    row, col, omega = self.find_backtracking_candidate()
                    backtrack_grid.update_cell(row, col, omega)
                    try:
                        if backtrack_grid.solve():
                            self.stage_list.append('Backtrack')
                            self.stage_list = self.stage_list + backtrack_grid.stage_list
                            self.grid = backtrack_grid.grid
                            return True
                        else:
                            self.prune_cells([self.grid[row][col]], [omega])
                    except:
                        self.stage_list.append('Backtrack prune')
                        self.prune_cells([self.grid[row][col]], [omega])
        return self.is_finished()