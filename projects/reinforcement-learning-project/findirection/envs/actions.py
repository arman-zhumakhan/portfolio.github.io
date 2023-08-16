from enum import IntEnum

class Actions(IntEnum):   
    Stay = 0
    North = 1
    East  = 2
    South = 3
    West  = 4

    def __str__(self): return self.name   