SIZE_MISMATCH_LABEL = "Size of domain and image of a cover must match."
class Cover:
    def __init__(self, domain, image):
        if len(domain) != len(image):
            raise Exception(SIZE_MISMATCH_LABEL)
        self.I = self.I = [i for i in range(len(domain))]
        self.domain = [domain[i] for i in self.I]
        self.image = [image[i] for i in self.I]

    def clear(self):
        self.sub_indexes = set()
        self.sub_image = set()
        self.valid_indexes = [index for index in self.I if (self.image[index] is not None and len(self.image[index]) <= self.m)]

    def get_sub_cover(self, m):
        self.m = m
        self.clear()
        if self.find_sub_cover(m):
            return [[self.domain[i] for i in self.sub_indexes], self.sub_image]
        else:
            return None

    def is_prunable(self, current_image):
        for image in current_image:
            for index in self.I:
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

    def find_sub_cover(self, cover_size):
        if cover_size == 2:
            return self.find_pair()
        else:
            valid_indexes = self.valid_indexes.copy()
            for index in valid_indexes:
                if index not in self.sub_indexes:
                    image = self.image[index]
                    self.sub_indexes.add(index)
                    last_sub_image = self.sub_image.copy()
                    self.sub_image = self.sub_image.union(image)
                    if len(self.sub_image) <= self.m and self.find_sub_cover(cover_size-1):
                        return True
                    self.sub_indexes.remove(index)
                    self.sub_image = last_sub_image
                if cover_size == self.m:
                    self.valid_indexes.remove(index)

            return False
