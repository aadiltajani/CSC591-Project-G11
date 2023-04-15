import utility as util
from cluster import *
import query as query

def sway(data):

    def worker(rows, worse, evals0, above = None):
        if len(rows) <= len(data.rows) ** util.args.min:
            return rows, many(worse, util.args.rest*len(rows)), evals0
        else:
            l , r, A, B, c, evals = half(data, rows, None, above)
            if query.better(data, B, A):
                l, r, A, B = r, l, B, A
            for row in r:
                worse.append(row)
            return worker(l, worse, evals + evals0, A)
    best, rest, evals = worker(data.rows, [], 0)
    return DATA(data, best), DATA(data, rest), evals
