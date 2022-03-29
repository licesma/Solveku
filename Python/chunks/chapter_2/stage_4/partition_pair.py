class Partition:
    """..."""
    def valid_result(self):
        for image in self.sub_image:
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
                    self.sub_image = current_image
                    if self.valid_result():
                        print(past_images[current_image])
                        print(index)
                        return True
                    else:
                        self.sub_indexes.remove(past_images[current_image])
                        self.sub_indexes.remove(index)
                else:
                    past_images[current_image] = index
        return False