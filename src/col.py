from num import NUM
from sym import SYM

class COL:
    def __init__(self, n, s):
        s = s.strip()
        self.col = NUM(n, s) if s[0].isupper() else SYM(n, s)
        self.isIgnored = self.col.txt.endswith("X")
        self.isKlass = self.col.txt.endswith("!")
        self.isGoal = self.col.txt[-1] in ["!", "+", "-"]
