
class CDict:

    def __init__(self, min_range, max_range):
        self.min_range = min_range
        self.max_range = max_range
        self.data = {}

    def error(self):
        print("Error, array index out of bounds")

    def add(self, key, value):
        if key <= self.max_range and key >= self.min_range and isinstance(key, int):
            self.data[key] = value
        else:
            self.error()

    def get(self, key):
        if key <= self.max_range and key >= self.min_range and isinstance(key, int):
            return self.data[key]
        else:
            self.error()

    def __str__(self):
        return str(self.data)

table = CDict(2, 4)
table.add(2, 5) # key -- value
print(table.get(2))