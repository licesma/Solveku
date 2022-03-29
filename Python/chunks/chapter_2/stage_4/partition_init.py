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
