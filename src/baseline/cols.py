from num import NUM
from sym import SYM
from col import COL
import re

class COLS:
    def __init__(self, ss):
        self.names = ss
        self.all = []
        self.x = []
        self.y = []
        for n, s in enumerate(ss):
            col = COL(n, s)
            self.all.append(col)
            if not col.isIgnored:
                if hasattr(col, 'isKlass') and col.isKlass:
                    self.klass = col
                if col.isGoal:
                    self.y.append(col)
                else:
                    self.x.append(col)
