from cols import COLS
import utility as util
import stats
import random

def row(data, t):
    if data.cols:
        data.rows.append(t)
        for cols in [data.cols.x, data.cols.y]:
            for col in cols:
                add(col.col, t[col.col.at])
    else:
        data.cols = COLS(t)
    return data


def add(col, x, n = None):
    def sym(t):
        t[x] = n + (t.get(x, 0))
        if t[x] > col.most:
            col.most, col.mode = t[x], x

    def num(t):
        col.lo, col.hi = min(x, col.lo), max(x, col.hi)
        if len(t) < util.args.Max:
            col.ok = False
            t.append(x)
        elif stats.rand() < util.args.Max / col.n:
            col.ok = False
            t[stats.rint(0, len(t) - 1)] = x

    if x != "?":
        n = n or 1
        col.n += n
        if hasattr(col, "isSym") and col.isSym:
            sym(col.has)
        else:
            x = float(x)
            num(col.has)

def adds(col, t):
    for value in t or []:
        add(col, value)
    return col

def extend(range, n, s):
    range.lo = min(n, range.lo)
    range.hi = max(n, range.hi)
    add(range.y, s)
