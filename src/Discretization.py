from col import COL
from range import *
import update as update
from query import *
import utility as util
import math
from copy import deepcopy
import list as lst
from rule import RULE

def bins(cols, rowss):

    out = []
    for col in cols:
        ranges = {}
        for y, rows in rowss.items():
            for row in rows:
                if (isinstance(col, COL)):
                    col = col.col
                x = row[col.at]
                if x != "?":
                    k = bin(col, float(x) if x != "?" and hasattr(col, "isSym") == False else x)
                    ranges[k] = ranges[k] if k in ranges else RANGE(col.at, col.txt, float(x) if x != "?"  and hasattr(col, "isSym") == False else x)
                    update.extend(ranges[k], float(x) if not hasattr(col, "isSym") else x, y)
        ranges = {key: value for key, value in sorted(ranges.items(), key=lambda x: x[1].lo)}
        newRanges = {}
        i = 0
        for key in ranges:
            newRanges[i] = ranges[key]
            i += 1
        newRangesList = []
        if hasattr(col, "isSym") and col.isSym:
            for item in newRanges.values():
                newRangesList.append(item)
        out.append(newRangesList if hasattr(col, "isSym") and col.isSym else mergeAny(newRanges))
    return out

def bin(col, x):

    if x=="?" or hasattr(col, "isSym"):
        return x
    tmp = (col.hi - col.lo)/(util.args.bins - 1)
    return 1 if col.hi == col.lo else math.floor(x / tmp + 0.5) * tmp

def mergeAny(ranges0):

    def noGaps(t):
        for j in range(1, len(t)):
            t[j].lo = t[j-1].hi
        t[0].lo = -float("inf")
        t[-1].hi = float("inf")
        return t
    ranges1, j = [], 0
    while j < len(ranges0):
        left, right = ranges0[j], ranges0[j+1] if j + 1 < len(ranges0) else None
        if right:
            y = merge2(left.y, right.y)
            if y:
               j = j+1
               left.hi, left.y = right.hi, y
        ranges1.append(left)
        j += 1
    return noGaps(ranges0) if len(ranges1)==len(ranges0) else mergeAny(ranges1)

def merge2(col1, col2):

    new = merge(col1, col2)
    if div(new) <= (div(col1)*col1.n + div(col2)*col2.n)/new.n:
        return new

def merge(col1, col2):

    new = deepcopy(col1)
    if hasattr(col1, "isSym") and col1.isSym:
        for x, n in col2.has.items():
            add(new, x, n)
    else:
        for n in col2.has:
            add(new, n)
        new.lo = min(col1.lo, col2.lo)
        new.hi = max(col1.hi, col2.hi)
    return new

def xpln(data, best, rest):
    def v(has):
        return value(has, len(best.rows), len(rest.rows), "best")
    def score(ranges):
        rule = RULE(ranges, maxSizes)
        if rule:
            bestr= selects(rule, best.rows)
            restr= selects(rule, rest.rows)
            if len(bestr) + len(restr) > 0:
                return v({"best": len(bestr), "rest": len(restr)}), rule
    tmp, maxSizes = [], {}
    for ranges in bins(data.cols.x, {"best": best.rows, "rest": rest.rows}):
        maxSizes[ranges[0].txt] = len(ranges)
        for range in ranges:
            tmp.append({"range": range, "max": len(ranges), "val": v(range.y.has)})

    rule, most = firstN(sorted(tmp, key=lambda x: x["val"], reverse=True), score)
    return rule, most


def firstN(sortedRanges, scoreFun):
    first = sortedRanges[0]["val"]
    def useful(range):
        if range["val"] > 0.05 and range["val"] > first / 10:
            return range

    sortedRanges = list(filter(useful, sortedRanges))
    most, out = -1, None

    for n in range(len(sortedRanges)):
        tmp, rule = scoreFun([r["range"] for r in sortedRanges[:n + 1]]) or (None, None)

        if tmp and tmp > most:
            out, most = rule, tmp

    return out, most



def showRule(rule):
    def pretty(range):
        return range['lo'] if range['lo'] == range['hi'] else [range['lo'], range['hi']]

    def merges(attr, ranges):
        return list(map(pretty, merge(sorted(ranges, key=lambda r: r['lo'])))), attr

    def merge(t0):
        t, j = [], 0
        while j < len(t0):
            left, right = t0[j], t0[j+1] if j+1 < len(t0) else None
            if right and left['hi'] == right['lo']:
                left['hi'] = right['hi']
                j += 1
            t.append({'lo': left['lo'], 'hi': left['hi']})
            j += 1
        return t if len(t0) == len(t) else merge(t)

    return lst.kap(rule, merges)

def selects(rule, rows):
    def disjunction(ranges, row):
        for range in ranges:
            lo = range['lo']
            hi = range['hi']
            at = int(range['at'])
            x = row[at]
            if x == "?":
                return True
            x = float(x) if x.replace(".", "").isnumeric() else x
            if lo == hi: 
                if lo == x:
                    return True
                else:
                    return False
            if lo <= x and x < hi:
                return True
        return False

    def conjunction(row):
        for ranges in rule.values():
            if not disjunction(ranges, row):
                return False
        return True

    return [r for r in rows if conjunction(r)]

def xpln2(data, best, rest):
    def v(has):
        return value(has, len(best.rows), len(rest.rows), "best")
    def score(ranges, negranges):
        rule = {'pos':RULE(ranges, maxSizes), 'neg':RULE(negranges, maxSizes)}
        if rule['pos']:
            bestr= selects2(rule, best.rows)
            restr= selects2(rule, rest.rows)
            if len(bestr) + len(restr) > 0:
                return v({"best": len(bestr), "rest": len(restr)}), rule
    tmp, maxSizes = [], {}
    for ranges in bins(data.cols.x, {"best": best.rows, "rest": rest.rows}):
        maxSizes[ranges[0].txt] = len(ranges)
        for range in ranges:
            tmp.append({"range": range, "max": len(ranges), "val": v(range.y.has)})

    rule, most = firstN2(sorted(tmp, key=lambda x: x["val"], reverse=True), score)
    return rule, most

def firstN2(sortedRanges, scoreFun):
    first = sortedRanges[0]["val"]
    def useful(range):
        if range["val"] > 0.05 and range["val"] > first / 10:
            return range
        
    def neg(range):
        if range["val"] < 0.05 and range["val"] < first / 10:
            return range

    negranges = list(filter(neg, sortedRanges))
    negranges.reverse()
    sortedRanges = list(filter(useful, sortedRanges))
    most, out = -1, None

    for n in range(len(sortedRanges)):
        tmp, rule = scoreFun([r["range"] for r in sortedRanges[:n + 1]], [r["range"] for r in negranges[:]]) or (None, None)

        if tmp and tmp > most:
            out, most = rule, tmp

    return out, most


def selects2(rule, rows):
    def disjunction(ranges, row):
        for range in ranges:
            lo = range['lo']
            hi = range['hi']
            at = int(range['at'])
            x = row[at]
            if x == "?":
                return True
            x = float(x) if x.replace(".", "").isnumeric() else x
            if lo == hi: 
                if lo == x:
                    return True
                else:
                    return False
            if lo <= x and x < hi:
                return True
        return False

    def conjunction(row):
        for ranges in rule['pos'].values():
            for neg in rule['neg'].values():
                if disjunction(neg, row):
                    return False
            if not disjunction(ranges, row):
                return False
        return True

    return [r for r in rows if conjunction(r)]