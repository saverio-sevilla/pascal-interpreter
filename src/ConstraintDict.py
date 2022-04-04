# Used to represent static arrays in the stack
import sys
import logging


class CDict:

    def __init__(self, min_range = 0, max_range = 0):
        self.min_range = min_range
        self.max_range = max_range
        self.data = {}

    def error(self):
        print("Error: array index out of bounds")
        sys.exit()

    def reshape(self, min_range, max_range):
        if min_range < 0 or max_range < 0:
            logging.error("Array bounds are not valid")
            sys.exit()
        self.min_range = min_range
        self.max_range = max_range
        logging.debug("Array resized with bounds {b1}:{b2}".format(b1=min_range, b2=max_range))

    def set_length(self, length):
        self.min_range = 0
        self.max_range = length
        if not self.data:
            self.data = dict.fromkeys(range(length),0)
            logging.debug("Array initialised to size {length}".format(length=length))

    def add(self, key, value):
        if self.max_range >= key >= self.min_range and isinstance(key, int):
            self.data[key] = value
        else:
            logging.error("Attempted to assign to an array value out of bounds")
            sys.exit()

    def get(self, key):
        if self.max_range >= key >= self.min_range and isinstance(key, int):
            return self.data[key]
        else:
            logging.error("Attempted to access an array value out of bounds")
            sys.exit()

    def __str__(self):
        return str(self.data)

