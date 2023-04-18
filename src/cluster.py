from query import *
from data import *
import utility as util

def half2(data, rows = None, cols = None, above = None):

        def gap(r1, r2):
            return dist(data, r1, r2, cols)
        def cos(a, b, c):
            return (a**2 + c**2 - b**2)/(2*c)
        def proj(r):
            return {'row': r, 'x': cos(gap(r, A), gap(r, B), c)}
        rows = rows or data.rows
        some = many(rows, util.args.Halves)
        newA = []
        for j in data.cols.all:
            i = j.col
            if i.txt[0].isupper():
                mu = i.lo + (i.hi - i.lo)/2
                if i.txt[-1] in "X":
                    newA.append(mu)
                elif i.txt[-1] in "+-!":
                    newA.append(i.lo-mu if i.txt[-1]=="-" else i.hi+mu)
                else:
                    rdata = any(i.has)
                    newA.append(rdata)
            else:
                newA.append(any(list(i.has.keys())))

        # A = above if util.args.Reuse else any(some)
        tmp = sorted([{"row": r, "d": gap(r, [str(i) for i in newA])} for r in some], key=lambda x: x["d"])
        A =  tmp[0]['row']
        tmp = sorted([{"row": r, "d": gap(r, A)} for r in some], key=lambda x: x["d"])
        far = tmp[int(len(tmp)*util.args.Far)]
        B, c = far["row"], far["d"]
        sorted_rows = sorted(map(proj, rows), key=lambda x: x["x"])
        left, right = [], []
        for n, two in enumerate(sorted_rows[:-2]):
            if n <= (len(rows) - 1) / 2:
                left.append(two["row"])
            else:
                right.append(two["row"])
        evals = 1 if (hasattr(util.args, "Reuse") and above) else 2
        return left, right, A, B, c, evals

def half(data, rows = None, cols = None, above = None):

        def gap(r1, r2):
            return dist(data, r1, r2, cols)
        def cos(a, b, c):
            return (a**2 + c**2 - b**2)/(2*c)
        def proj(r):
            return {'row': r, 'x': cos(gap(r, A), gap(r, B), c)}
        rows = rows or data.rows
        some = many(rows, util.args.Halves)
        A = above if util.args.Reuse else any(some)
        tmp = sorted([{"row": r, "d": gap(r, A)} for r in some], key=lambda x: x["d"])
        far = tmp[int(len(tmp)*util.args.Far)]
        B, c = far["row"], far["d"]
        sorted_rows = sorted(map(proj, rows), key=lambda x: x["x"])
        left, right = [], []
        for n, two in enumerate(sorted_rows):
            if n <= (len(rows) - 1) / 2:
                left.append(two["row"])
            else:
                right.append(two["row"])
        evals = 1 if (hasattr(util.args, "Reuse") and above) else 2
        return left, right, A, B, c, evals

def tree(data, rows = None, cols = None, above = None):
    rows = rows if rows else data.rows
    here = {"data" : DATA(data, rows)}
    if len(rows)>=2*(len(data.rows) ** util.args.min):  # util.args.min needed where 0.5 is
        left, right, A, B, _, _ = half(data, rows, cols, above)
        here["left"] = tree(data, left, cols, A)
        here["right"] = tree(data, right, cols, B)
    return here

def showTree(tree, lvl=0):

    if tree:
        print("{}[{}]".format("|.. " * lvl, len(tree["data"].rows)), end="")
        if lvl == 0 or not "left" in tree:
            print(stats(tree["data"]))
        else:
            print("")
        showTree(tree["left"] if "left" in tree else None, lvl + 1)
        showTree(tree["right"] if "right" in tree else None, lvl + 1)
