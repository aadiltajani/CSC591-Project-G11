from list import *
from utility import *
import utility as util
import math
import sys
from functools import cmp_to_key

def has(col):

    if not hasattr(col, "isSym") and not col.ok:
        if isinstance(col.has, dict):
            col.has = dict(sorted(col.has.items(), key = lambda item: item[1]))
        else:
            col.has.sort()
    col.ok = True
    return col.has

def mid(col):

    return col.mode if hasattr(col, "isSym") else per(has(col), 0.5)

def div(col):

    if hasattr(col, "isSym"):
        e = 0
        if isinstance(col.has, dict):
            for n in col.has.values():
                e = e - n/col.n * math.log(n/col.n, 2)
        else:
            for n in col.col.has:
                e = e - n/col.col.n * math.log(n/col.colc.n, 2)
        return e
    else:
        return (per(has(col),.9) - per(has(col), .1)) / 2.58

def stats(data, fun = None, cols = None, nPlaces = 2):

    cols = cols or data.cols.y
    def callBack(k, col):
        col = col.col
        return round((fun or mid)(col), nPlaces), col.txt
    tmp = kap(cols, callBack)
    return tmp

def norm(num, n):
    return n if n == "?" else (float(n) - float(num.lo)) / (float(num.hi) - float(num.lo) + sys.float_info.min)


def value(has, nB = 1, nR = 1, sGoal = True):
    b, r = 0, 0
    for x, n in has.items():
        if x == sGoal:
            b += n
        else:
            r += n
    b,r = b/(nB+1/float("inf")), r/(nR+1/float("inf"))
    return (b ** 2) / (b + r)

def dist(data, t1, t2, cols=None, d=None, dist1=None, mode = None):
    def sym(x, y):
        return 0 if x == y else 1

    def num(x, y):
        x = float(x) if x!='?' else "?"
        y = float(y) if y!='?' else "?"
        if x == "?":
            x = 1 if y < 0.5 else 1
        if y == "?":
            y = 1 if x < 0.5 else 1
        return abs(x - y)

    def dist1(col, x, y):
        if x == "?" and y == "?":
            return 1
        return sym(x, y) if hasattr(col, "isSym") else num(norm(col,x), norm(col, y))

    d, cols = 0, cols or data.cols.x
    for col in cols:
        factor = 2 + 10/abs(col.col.hi - col.col.lo) if mode == 'sway2' else 1
        d += (dist1(col.col, t1[col.col.at], t2[col.col.at]) ** (util.args.p)) * factor
    return (d / len(cols)) ** (1 / util.args.p)


def better(data, row1, row2, mode = None):
    s1, s2, ys = 0, 0, data.cols.y
    for col in ys:
        # print(col.col.txt, col.col.isSym)
        x = norm(col.col, float(row1[col.col.at]) if row1[col.col.at] != "?" else row1[col.col.at])
        y = norm(col.col, float(row2[col.col.at]) if row2[col.col.at] != "?" else row2[col.col.at])
        factor = (2 + 10/abs(col.col.hi - col.col.lo)) if mode=='sway2' else 1
        s1 -= math.exp(col.col.w * (x-y)/len(ys)) ** factor
        s2 -= math.exp(col.col.w * (y-x)/len(ys)) ** factor

    return s1/len(ys) < s2 / len(ys)

def betters(data, n = None):
    tmp = sorted(data.rows, key=cmp_to_key(
            lambda row1, row2: -1 if better(data, row1, row2) else 1))
    return tmp[:n], tmp[n:] if n else tmp
