import math
import utility as util


def many(t, n):

    u = []
    for i in range(1, n + 1):
        u.append(any(t))
    return u

def any(t):
    rintVal = util.rint(None, len(t) - 1)
    return t[rintVal]

def per(t, p):
    if len(t) > 0:
        p = math.floor(((p or 0.5) * len(t)))
        return t[max(0, min(len(t) - 1, p))]
    else:
        return 0

def kap(listOfCols, fun):
    u = {}

    if isinstance(listOfCols, list):
        items = enumerate(listOfCols)
    else:
        items = listOfCols.items()

    for k, v in items:
            v, k = fun(k, v)
            u[k or len(u)+1] = v
    return u

def slice(t, go = None, stop = None, inc = None):
    if go and go < 0:
        go = len(t) - 1 + go
    if stop and stop < 0:
        stop = len(t) + stop
    u = []
    for j in range(int((go or 1)), int((stop or len(t))), int(inc or 1)):
        u.append(t[j])
    return u
