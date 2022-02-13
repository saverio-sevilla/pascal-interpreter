# Used to represent static arrays in the stack
import sys

class CDict:

    def __init__(self, min_range, max_range, dynamic=0):
        self.min_range = min_range
        self.max_range = max_range
        self.dynamic = dynamic
        self.data = {}

    def error(self):
        print("Error: array index out of bounds")
        sys.exit()

    def reshape(self, min_range, max_range):
        self.min_range = min_range
        self.max_range = max_range
        print("Array reshaped to", min_range, max_range)

    def add(self, key, value):
        if self.dynamic == 1:
            print("Cannot use dynamic array without initialization")
            sys.exit()
        if self.max_range >= key >= self.min_range and isinstance(key, int):
            self.data[key] = value
        else:
            self.error()

    def get(self, key):
        if self.max_range >= key >= self.min_range and isinstance(key, int):
            return self.data[key]
        else:
            self.error()

    def __str__(self):
        return str(self.data)
