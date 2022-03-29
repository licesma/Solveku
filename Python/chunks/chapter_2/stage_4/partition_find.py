class Partition:
    """..."""
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
                    if len(self.sub_image) <= self.m and self.find_sub_partition(partition_size - 1):
                        return True
                    self.sub_indexes.remove(index)
                    self.sub_image = last_sub_image
                if partition_size == self.m:
                    self.valid_indexes.remove(index)
            return False