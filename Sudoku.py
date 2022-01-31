class Cell:
    def __init__(self, value=0, fixed=False):
        self.value = value
        self.fixed = fixed
        self.a_set = set()


class Sudoku:

    def __init__(self, string_grid):
        self.create_grid(string_grid)
        self.create_row_set()
        self.create_col_set()
        self.create_box_set()

    def create_grid(self, string_grid):
        string_grid.pop(0)
        for ls in string_grid:
            ls.pop(0)
        self.grid = [[Cell(int(st), True) if st.isdigit() else Cell() for st in ls] for ls in string_grid]

    def get_grid(self):
        return [[c.value for c in ls] for ls in self.grid]

    def get_row(self, index):
        # Returns a list of all the cells' indexes in a particular row.
        return [(index, j) for j in range(9)]

    def get_available(self, index_list):
        return [pair for pair in index_list if self.grid[pair[0]][pair[1]].value == 0]

    def get_col(self, index):
        return [(i, index) for i in range(9)]

    def get_box_at(self, row, col):
        f_row = 3 * int(row / 3)
        f_col = 3 * int(col / 3)
        return [(i + f_row, j + f_col) for i in range(3) for j in range(3)]

    def get_box(self, index):
        return self.get_box_at(int(index / 3) * 3, (index % 3) * 3)

    def create_row_set(self):
        self.row_set = [
            {self.grid[row][col].value for (row, col) in self.get_row(i) if self.grid[row][col].value != 0} for i in
            range(9)]

    def create_col_set(self):
        self.col_set = [
            {self.grid[row][col].value for (row, col) in self.get_col(i) if self.grid[row][col].value != 0} for i in
            range(9)]

    def create_box_set(self):
        self.box_set = [
            {self.grid[row][col].value for (row, col) in self.get_box(i) if self.grid[row][col].value != 0} for i in
            range(9)]

    def find_cell_by_num(self, cell_list, num):
        for row, col in cell_list:
            a_set = self.grid[row][col].a_set
            if a_set is not None and num in a_set:
                return row, col
        return -1, -1

    def second_state(self):
        self.create_dics()
        if self.check_row_hermit() is None or self.check_col_hermit() is None or self.check_box_hermit() is None:
            self.first_stage()
        self.third_stage()

    def create_a_set(self):
        for row in range(9):
            for col in range(9):
                if self.grid[row][col].value == 0:
                    self.grid[row][col].a_set = {i + 1 for i in range(9)}.difference(
                        self.row_set[row].union(self.col_set[col]).union(self.box_set[self.box_of(row, col)]))

    def print_grid(self):
        for ls in self.grid:
            for c in ls:
                print(c.value)
                print(" ")
            print("\n")

    def box_of(self, row, col):
        return 3 * int(row / 3) + int(col / 3)

    # ________________________________________________________________________________________________________
    # ___________________________________GENERAL_________________________________________________________
    # ________________________________________________________________________________________________________

    def update_value(self, row, col, num):
        self.grid[row][col].a_set = None
        self.grid[row][col].value = num
        self.row_set[row].add(num)
        self.col_set[col].add(num)
        self.box_set[self.box_of(row, col)].add(num)

    # ________________________________________________________________________________________________________
    # ___________________________________FIRST STAGE_________________________________________________________
    # ________________________________________________________________________________________________________
    def first_stage(self):
        finish = False
        self.create_a_set()
        while not finish:
            finish = True
            for row in range(9):
                for col in range(9):
                    cell = self.grid[row][col]
                    if cell.value == 0 and len(cell.a_set) == 1:
                        finish = False
                        self.update_value(row, col, cell.a_set.pop())
            if not finish:
                self.create_a_set()
        self.second_stage()

    # ________________________________________________________________________________________________________
    # ___________________________________SECOND STAGE_________________________________________________________
    # ________________________________________________________________________________________________________
    def second_stage(self):
        print("Second Stage")
        self.define_dics()
        row_hermit = self.check_row_hermit()
        col_hermit = self.check_col_hermit()
        box_hermit = self.check_box_hermit()
        if row_hermit or col_hermit or box_hermit:
            self.first_stage()
            return
        print("Finish")

    def define_dics(self):
        self.row_dic = [{num + 1: 0 for num in range(9) if num + 1 not in self.row_set[index]} for index in range(9)]
        self.col_dic = [{num + 1: 0 for num in range(9) if num + 1 not in self.col_set[index]} for index in range(9)]
        self.box_dic = [{num + 1: 0 for num in range(9) if num + 1 not in self.box_set[index]} for index in range(9)]
        for row in range(9):
            for col in range(9):
                cell = self.grid[row][col]
                if cell.value == 0:
                    for num in cell.a_set:
                        self.row_dic[row][num] += 1
                        self.col_dic[col][num] += 1
                        self.box_dic[self.box_of(row, col)][num] += 1

    def check_row_hermit(self):
        res = False
        for index in range(9):
            dic = self.row_dic[index]
            for num, reps in dic.items():
                if reps == 1:
                    row, col = self.find_cell_by_num(self.get_row(index), num)
                    self.update_value(row, col, num)
                    self.first_stage()
                    res = True
        return res

    def check_col_hermit(self):
        res = False
        for index in range(9):
            dic = self.col_dic[index]
            for num, reps in dic.items():
                if reps == 1:
                    row, col = self.find_cell_by_num(self.get_col(index), num)
                    self.update_value(row, col, num)
                    self.first_stage()
                    res = True
        return res

    def check_box_hermit(self):
        res = False
        for index in range(9):
            dic = self.box_dic[index]
            for num, reps in dic.items():
                if reps == 1:
                    row, col = self.find_cell_by_num(self.get_box(index), num)
                    self.update_value(row, col, num)
                    self.first_stage()
                    res = True
        return res

    # ________________________________________________________________________________________________________
    # ___________________________________THIRD STAGE_________________________________________________________
    # ________________________________________________________________________________________________________
    def third_stage(self):
        def b_of(pair):
            return self.box_of(pair[0], pair[1])
        def r_of(pair):
            return pair[0]
        def c_of(pair):
            return pair[1]
        res = False
        for i in range(9):
            row_res = self.check_outer_gp(self.get_row(i), b_of, self.get_box)
            col_res = self.check_outer_gp(self.get_col(i), b_of, self.get_box)
            box_r_res = self.check_outer_gp(self.get_box(i), r_of, self.get_row)
            box_c_res = self.check_outer_gp(self.get_box(i), c_of, self.get_col)
            res = res or row_res or col_res or box_r_res or box_c_res
        print(res)

    def outer_prune(self, prune_list, exception_list, num):
        res = False
        for pair in prune_list:
            cell = self.grid[pair[0]][pair[1]]
            if cell.value == 0 and pair not in exception_list and num in cell.a_set:
                cell.a_set.remove(num)
                res = True
        return res

    def check_outer_gp(self, list_pair, split_f, list_prune_f):
        res = False
        list_pair_av = self.get_available(list_pair)
        for num in range(1, 10):
            split_value = -1
            for pair in list_pair_av:
                cell = self.grid[pair[0]][pair[1]]
                if num in cell.a_set:
                    current_value = split_f(pair)
                    if split_value == -1:
                        split_value = current_value
                    elif split_value != current_value:
                        split_value = -1
                        break
            if split_value != -1:
                prune_res = self.outer_prune(list_prune_f(split_value), list_pair_av, num)
                res = res or prune_res
        return res








