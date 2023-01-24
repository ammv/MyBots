class PostStack:
    def __init__(self, size=10, pointer=0):
        self.size = size
        self.pointer = pointer
        self.inc_pointer = int(self.size != 1)
        self.items = [None] * self.size
        
    def _add(self, item):
        if item not in self.items:
            self.items[self.pointer] = item

            if self.pointer + 1 == self.size:
                self.pointer = 0
            else:
                self.pointer += self.inc_pointer
        
    def add(self, *item):
        for i in item:
            self._add(i['id'])

    def from_data(self, data):
        self.items[0:self.size] = data[0:self.size]

    def get_file_version(self):
        return [self.pointer] + self.items
            