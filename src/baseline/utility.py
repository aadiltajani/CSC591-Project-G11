import argparse
import csv
import json
import math
import os
from num import NUM
from sym import SYM
from data import DATA
from update import *
import query as query
import miscellaneous as misc
import cluster as cluster
import Optimization as opt
import Discretization as disc


args = None
Seed = None
egs = {}
n = 0

def dofile(filename):
    with open(filename) as f:
        return json.load(f)

def rint(lo = None, hi = None):

    return math.floor(0.5 + rand(lo, hi))

def rand(low = None, high = None):
    global Seed
    # if Seed in [937162211, 11234]:
    #     print(Seed)
    low, high = low or 0, high or 1
    Seed = (16807 * Seed) % 2147483647
    return low + (high - low) * Seed / 2147483647

def eg(key, string, fun):
    global egs
    global help
    egs[key] = fun
    help += f"  -g {key}    {string}"

# def oo():
#     pass

# def randFunc():

#     global args
#     global Seed
#     Seed = 1
#     t = []
#     for i in range(1000):
#         t.append(rint(100))
#     Seed = 1
#     u = []
#     for i in range(1000):
#         u.append(rint(100))
#     Seed = 937162211
#     for index, value in enumerate(t):
#         if (value != u[index]):
#             return False
#     return True

# def someFunc():
#     global args
#     args.Max = 32
#     num1 = NUM()
#     for i in range(10000):
#         add(num1, i)
#     args.Max = 512
    # print(has(num1))

# def symFunc():
#     sym = adds(SYM(), ["a","a","a","a","b","b","c"])
#     print(query.mid(sym), round(query.div(sym), 2))
#     return 1.38 == round(query.div(sym), 2)

# def numFunc():
#     num1, num2 = NUM(), NUM()
#     for i in range(10000):
#         add(num1, rand())
#     for i in range(10000):
#         add(num2, rand() ** 2)
#     print(1, round(query.mid(num1), 2), round(query.div(num1), 2))
#     print(2, round(query.mid(num2), 2), round(query.div(num2), 2))
#     return .5 == round(query.mid(num1), 1) and query.mid(num1)> query.mid(num2)

# def crashFunc():
#     num = NUM()
#     return not hasattr(num, 'some.missing.nested.field')

def getCliArgs(seed):
    global args
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-b", "--bins", type=int, default=16, required=False, help="initial number of bins")
    parser.add_argument("-d", "--d", type=float, default=0.35, required=False, help="different is over sd*d")
    parser.add_argument("-g", "--go", type=str, default="all", required=False, help="start-up action")
    parser.add_argument("-h", "--help", action='store_true', help="show help")
    parser.add_argument("-s", "--seed", type=int, default=seed, required=False, help="random number seed")
    parser.add_argument("-f", "--file", type=str, default="../../etc/data/healthCloseIsses12mths0001-hard.csv", required=False, help="data file")
    parser.add_argument("-p", "--p", type=int, default=2, required=False, help="distance coefficient")
    parser.add_argument("-c", "--cliffs", type=float, default=0.147, required=False, help="cliff's delta threshold")
    parser.add_argument("-F", "--Far", type=float, default=0.95, required=False, help="distance to distant")
    parser.add_argument("-H", "--Halves", type=int, default=512, required=False, help="search space for clustering")
    parser.add_argument("-m", "--min", type=float, default=0.5, required=False, help="size of smallest cluster")
    parser.add_argument("-M", "--Max", type=int, default=512, required=False, help="numbers")
    parser.add_argument("-r", "--rest", type=int, default=4, required=False, help="how many of rest to sample")
    parser.add_argument("-R", "--Reuse", type=bool, default=False, required=False, help="child splits reuse a parent pole")

    args = parser.parse_args()

def csvFunc():
    global n
    def fun(t):
        global n
        n += len(t)
    script_dir = os.path.dirname(__file__)
    full_path = os.path.join(script_dir, args.file)
    readCSV(full_path, fun)
    return n == 8 * 399

def readCSV(sFilename, fun):
    with open(sFilename, mode='r') as file:
        csvFile = csv.reader(file)
        for line in csvFile:
            fun(line)

# def swayFunc():
#     for mode in ["sway1", "sway2"]:
#         print("sway mode:",mode)
#         script_dir = os.path.dirname(__file__)
#         full_path = os.path.join(script_dir, args.file)
#         data = DATA(full_path)
#         best, rest, _ = opt.sway(mode, data)
#         print("\nall ", query.stats(data))
#         print("    ",   query.stats(data, query.div))
#         print("\nbest", query.stats(best))
#         print("    ",   query.stats(best, query.div))
#         print("\nrest", query.stats(rest))
#         print("    ",   query.stats(rest, query.div))
#         print("\nall ~= best?", misc.diffs(best.cols.y, data.cols.y))
#         print("best ~= rest?", misc.diffs(best.cols.y, rest.cols.y))


def cliffsFunc():

    assert misc.cliffsDelta([8, 7, 6, 2, 5, 8, 7, 3], [8, 7, 6, 2, 5, 8, 7, 3]) == False, "First cliff fails"
    assert misc.cliffsDelta([8, 7, 6, 2, 5, 8, 7, 3], [9, 9, 7, 8, 10, 9, 6]) == True, "Second cliff fails"
    t1, t2 = [], []
    for i in range(1000):
        t1.append(rand())
        t2.append(math.sqrt(rand()))
    assert misc.cliffsDelta(t1, t1) == False, "Third cliff fails"
    assert misc.cliffsDelta(t1, t2) == True, "Fourth cliff fails"
    diff, j = False, 1.0
    while not diff:
        t3 = list(map(lambda x: x*j, t1))
        diff = misc.cliffsDelta(t1, t3)
        print(">", round(j, 4), diff)
        j *= 1.025

# def distFunc():

#     script_dir = os.path.dirname(__file__)
#     full_path = os.path.join(script_dir, args.file)
#     data = DATA(full_path)
#     num  = NUM()
#     for row in data.rows:
#         add(num, query.dist(data, row, data.rows[0]))
#     print({"lo": num.lo, "hi": num.hi, "mid": round(query.mid(num)), "div": round(query.div(num))})

# def treeFunc():

#     script_dir = os.path.dirname(__file__)
#     full_path = os.path.join(script_dir, args.file)
#     data = DATA(full_path)
#     cluster.showTree(cluster.tree(data))

# def binsFunc():

#     script_dir = os.path.dirname(__file__)
#     full_path = os.path.join(script_dir, args.file)
#     data = DATA(full_path)
#     best, rest, _ = opt.sway(data)
#     b4 = None
#     print("all","","","", "{best= " + str(len(best.rows)) + ", rest= " + str(len(rest.rows)) + "}")
#     result = disc.bins(data.cols.x, {"best": best.rows, "rest": rest.rows})
#     for t in result:
#         for range in t:
#             if range.txt != b4:
#                 print("")
#             b4 = range.txt
#             print(range.txt,
#                   range.lo,
#                   range.hi,
#                   round(query.value(range.y.has, len(best.rows), len(rest.rows), "best")),
#                   range.y.has)

def explnFunc():
    global Seed
    Seed = util.args.seed
    val = {}
    # val1 = {}        
    # val2 = {}

    # for mode in ["sway1"]:
        # Seed = util.args.seed
        # print("\n\n_______________xpln1 sway:", mode)
    script_dir = os.path.dirname(__file__)
    full_path = os.path.join(script_dir, args.file)
    data = DATA(full_path)
    best, rest, evals = opt.sway("sway1", data)
    val['all'] = query.stats(data)
    val["sway1"] = query.stats(best)
    rule, _ = disc.xpln(data, best, rest)
    # print("\n-----------\nexplain=", disc.showRule(rule))
    data1 = DATA(data, disc.selects(rule, data.rows))
    val['xpln1'] = query.stats(data1)
        # print("all                ", query.stats(data), query.stats(data, query.div))
        # print(f"sway with   {evals} evals", query.stats(best), query.stats(best, query.div))
        # print(f"xpln on     {evals} evals", query.stats(data1), query.stats(data1, query.div))
    top, _ = query.betters(data, 1)
        # print("__top:", top)
        # print("\n\n__",_)
    top = DATA(data, top)
    val['top'] = query.stats(top)
        # print(f"sort with {len(data.rows)} evals", query.stats(top), query.stats(top, query.div))
    # for mode in ["sway2"]:
    Seed = util.args.seed
    # print("\n\n_______________xpln2 sway:", mode)
    script_dir = os.path.dirname(__file__)
    full_path = os.path.join(script_dir, args.file)
    data = DATA(full_path)
    best, rest, evals = opt.sway("sway2", data)
    val["sway2"] = query.stats(best)
    rule, _ = disc.xpln2(data, best, rest)
    # print("\n-----------\nexplain=", disc.showRule(rule['pos']), disc.showRule(rule['neg']))
    data1 = DATA(data, disc.selects2(rule, data.rows))
    val['xpln2'] = query.stats(data1)
        # print("all                ", query.stats(data), query.stats(data, query.div))
        # print(f"sway with   {evals} evals", query.stats(best), query.stats(best, query.div))
        # print(f"xpln on     {evals} evals", query.stats(data1), query.stats(data1, query.div))
        # top, _ = query.betters(data, len(best.rows))
        # top = DATA(data, top)
        # print(f"sort with {len(data.rows)} evals", query.stats(top), query.stats(top, query.div))
    # print("all",val['all'],sep='\t')
    # print("sway1",val1['sway1'],sep='\t')
    # print("xpln1",val1['sway1xpln1'],sep='\t')
    # print("sway2",val2['sway2'],sep='\t')
    # print("xpln2",val2['sway2xpln2'],sep='\t')
    # print("top",val['top'],sep='\t')
    return val