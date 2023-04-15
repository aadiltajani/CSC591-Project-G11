import math

class SYM:
    def __init__(self, n = 0, s = ""):
        self.at = n
        self.txt = s
        self.n = 0
        self.has = {}
        self.most = 0
        self.mode = None
        self.isSym = True
