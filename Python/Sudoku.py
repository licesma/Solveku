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
            return True
        return False

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

    def define_partitions(self):
        self.partitions = [Partition(SudokuGrid.I, [cell.av_set for cell in bracket]) for bracket in self.all]

    def inverse_av_set(self, bracket):
         raw_av_sets = [{i for i in SudokuGrid.I if bracket[i].av_set is not None and omega in bracket[i].av_set} for omega in
         SudokuGrid.Omega]
         return [av_set if 1 <= len(av_set) else None for av_set in raw_av_sets]

    def define_inverse_partitions(self):
        self.inverse_partitions = [Partition(SudokuGrid.Omega, self.inverse_av_set(bracket) ) for bracket in self.all]


    def get_orthogonal_partition(self, bracket, omega):
        res = {cell_index for cell_index in SudokuGrid.I if bracket[cell_index].av_set is not None and omega in bracket[cell_index].av_set}
        return res if res else None

    def define_orthogonal_partitions(self):
        self.orthogonal_row_partition = {
            omega: Partition(SudokuGrid.I, [self.get_orthogonal_partition(bracket, omega) for bracket in self.row])
            for omega in SudokuGrid.Omega}
        self.orthogonal_col_partition = {
            omega: Partition(SudokuGrid.I, [self.get_orthogonal_partition(bracket, omega) for bracket in self.col])
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
        self.all_images = [set() for _ in range(3 * sudoku.n)]
        self.rowImage = [self.all_images[i] for i in range(sudoku.n)]
        self.colImage = [self.all_images[i] for i in range(sudoku.n, 2 * sudoku.n)]
        self.boxImage = [self.all_images[i] for i in range(2 * sudoku.n, 3 * sudoku.n)]
        for i in sudoku.I:
            self.rowImage[i] = self.get_image(i)
            self.colImage[i] = self.get_image(sudoku.n + i)
            self.boxImage[i] = self.get_image(2*sudoku.n + i)


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

    def is_prunable(self):
        for image in self.sub_image:
            for index in SudokuGrid.I:
                if index not in self.sub_indexes and self.image[index] is not None and image in self.image[index]:
                    print(self.domain[index], 'image: ', image , 'in ', self.image[index])
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
                    if self.is_prunable():
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

    @staticmethod
    def box_of(row, col):
        root = int(math.sqrt(SudokuGrid.n))
        return root*int(row/root) + int(col/root)

    def box_cells(self, index):
        root = int(math.sqrt(self.n))
        start_row = root * int(index / root)
        start_col = root * int(index % root)
        return [self.grid[start_row + i][start_col + j] for i in range(root) for j in range(root)]

    def define_available_sets(self):
        for row in self.I:
            for col in self.I:
                cell = self.grid[row][col]
                if not cell.has_value():
                    for val in self.Omega:
                        if val in self.brackets.rowImage[row] or val in self.brackets.colImage[col] or val in self.brackets.boxImage[self.box_of(row, col)]:
                            cell.av_set.remove(val)

    def update_neighbors_available_set(self, row, col, num):
        for it in self.I:
            self.brackets.row[row][it].av_set_remove(num)
            self.brackets.col[col][it].av_set_remove(num)
            self.brackets.box[self.box_of(row,col)][it].av_set_remove(num)

    def update_cell(self, row, col, num):
        self.grid[row][col].value = num
        self.grid[row][col].av_set = None
        if num in self.brackets.rowImage[row] or num in self.brackets.colImage[col] or num in self.brackets.boxImage[self.box_of(row,col)]:
            raise Exception("Group constraint violated")
        self.brackets.rowImage[row].add(num)
        self.brackets.colImage[col].add(num)
        self.brackets.boxImage[self.box_of(row,col)].add(num)
        self.update_neighbors_available_set(row, col, num)

    def stage_one(self):
        changes = False
        for row in self.I:
            for col in self.I:
                cell = self.grid[row][col]
                if not cell.has_value() and len(cell.av_set) == 1:
                    changes = True
                    for num in cell.av_set:
                        self.update_cell(row, col, num)
        if changes:
            self.stage_one()
        else:
            self.stage_two()

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
            for candidate, cell_index in candidate_map.items():
                if 0 <= cell_index :
                    row = self.brackets.get_row(bracket_index, cell_index)
                    col = self.brackets.get_col(bracket_index, cell_index)
                    self.update_cell(row, col, candidate)
                    changes = True
        if changes:
            self.stage_two()

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
        res = False
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
                if target_index in SudokuGrid.I:
                    target_bracket = self.get_target_bracket(root_index, target_index, root_type, target_type)
                    prune_res = self.prune_bracket(target_bracket, intersection_map[candidate], candidate)
                    res = res or prune_res
        return res

    def stage_three(self):
        row_intersections = self.find_intersection(self.brackets.box, self.root_div, box_type, row_type)
        col_intersections = self.find_intersection(self.brackets.box, self.root_mod, box_type, col_type)
        box_r_intersections = self.find_intersection(self.brackets.row, self.root_div, row_type, box_type)
        box_c_intersections = self.find_intersection(self.brackets.col, self.root_div, col_type, box_type)

    def prune_cells(self, cells, values):
        """
        for cell in cells:
            for omega in values:
                cell.av_set_remove(omega)
        """
        x = 2

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

    def define_orthogonal_partitions(self):
        self.brackets.define_orthogonal_partitions()

    def prune_orthogonal_difference(self, prune_brackets, skip_indexes, omega):
        for bracket in prune_brackets:
            for index in SudokuGrid.I:
                if index not in skip_indexes:
                    bracket[index].av_set_remove(omega)

    def find_orthogonal_subset(self, source_partitions, orthogonal_brackets, m, source_str, normal_str):
        for omega, partition in source_partitions.items():
            sub_partition = partition.get_sub_partition(m)
            if sub_partition is not None:
                skip_indexes, prune_indexes = sub_partition
                prune_brackets = [orthogonal_brackets[index] for index in prune_indexes]
                self.prune_orthogonal_difference(prune_brackets, skip_indexes, omega)
                print(source_str, skip_indexes, ' ', normal_str, prune_indexes, ' ', omega)
                return True
        return False

    def stage_five(self, m):
        return self.find_orthogonal_subset(self.brackets.orthogonal_row_partition, self.brackets.col, m, 'rows', 'cols') or self.find_orthogonal_subset(self.brackets.orthogonal_col_partitional, self.brackets.row, m, 'cols', 'rows')




    def solve(self):
        self.define_orthogonal_partitions()
        max_partition_length = int(self.n/2)
        for i in range(3, max_partition_length+1):
            if self.stage_five(i):
                break

    def __init__(self, number_grid):
        self.grid = [[SudokuCell(num, True) if num != 0 else SudokuCell() for num in row] for row in number_grid]
        for row in self.I:
            for col in self.I:
                cell = self.grid[row][col]
                if not cell.has_value():
                    for val in self.Omega:
                        cell.av_set.add(val)
        self.brackets = Bracket(self)
        self.define_available_sets()

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
