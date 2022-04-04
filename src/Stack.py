#############
#  Stack    #
#############

from enum import Enum

class ARType(Enum):
    PROGRAM   = 'PROGRAM'
    PROCEDURE = 'PROCEDURE'
    FUNCTION  = 'FUNCTION'


class Frame(object):
    def __init__(self, name: str, type: ARType, nesting_level):
        # Change: nesting_level not set in new version
        # Change: add enclosing frame
        self.name = name
        self.type = type
        self.nesting_level = nesting_level
        self.return_value = None
        self.members = {}

    def __setitem__(self, key, value):
        self.members[key] = value

    def __getitem__(self, key):
        return self.members[key]

    def get(self, key):
        return self.members.get(key)

    def __str__(self):
        lines = [
            '{level}: {type} {name}'.format(
                level=self.nesting_level,
                type=self.type.value,
                name=self.name,
            )
        ]
        for name, val in self.members.items():
            lines.append(f'   {name:<20}: {val}')

        s = '\n'.join(lines)
        return s

    def __repr__(self):
        return self.__str__()


class CallStack(object):
    def __init__(self):
        self.frames = []

    def push(self, ar):  # change methods
        self.frames.append(ar)

    def pop(self):
        return self.frames.pop()

    def peek(self):
        if len(self.frames) is 0:
            return None
        return self.frames[-1]

    def __str__(self):
        s = '\n'.join(repr(ar) for ar in reversed(self.frames))
        s = f'CALL STACK\n{s}\n'
        return s

    def __repr__(self):
        return self.__str__()

