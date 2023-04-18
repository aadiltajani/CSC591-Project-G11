class NUM:
    def __init__(self, n = 0, s = "", ):
        self.at = n
        self.txt = s
        self.n = 0
        self.lo = float('inf')
        self.hi = float('-inf')
        self.ok = True
        self.has = []
        self.mu = 0
        self.m2 = 0
        self.sd = 0
        self.w = -1 if s.endswith("-") else 1
