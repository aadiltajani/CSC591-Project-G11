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

help = """
bins: multi-objective semi-supervised discetization
(c) 2023 Tim Menzies <timm@ieee.org> BSD-2

USAGE: lua bins.lua [OPTIONS] [-g ACTIONS]

OPTIONS:
  -b  --bins    initial number of bins       = 16
  -c  --cliffs  cliff's delta threshold      = .147
  -d  --d       different is over sd*d       = .35
  -f  --file    data file                    = ../etc/data/auto93.csv
  -F  --Far     distance to distant          = .95
  -g  --go      start-up action              = all
  -h  --help    show help                    = false
  -H  --Halves  search space for clustering  = 512
  -m  --min     size of smallest cluster     = .5
  -M  --Max     numbers                      = 512
  -p  --p       dist coefficient             = 2
  -r  --rest    how many of rest to sample   = 4
  -R  --Reuse   child splits reuse a parent pole = false
  -s  --seed    random number seed           = 937162211
"""

args = None
Seed = 937162211
egs = {}
n = 0

def dofile(filename):
    with open(filename) as f:
        return json.load(f)

def rint(lo = None, hi = None):

    return math.floor(0.5 + rand(lo, hi))

def rand(low = None, high = None):
    global Seed
    low, high = low or 0, high or 1
    Seed = (16807 * Seed) % 2147483647
    return low + (high - low) * Seed / 2147483647

def eg(key, string, fun):
    global egs
    global help
    egs[key] = fun
    help += f"  -g {key}    {string}"

def oo():
    pass

def randFunc():

    global args
    global Seed
    Seed = 1
    t = []
    for i in range(1000):
        t.append(rint(100))
    Seed = 1
    u = []
    for i in range(1000):
        u.append(rint(100))
    Seed = 937162211
    for index, value in enumerate(t):
        if (value != u[index]):
            return False
    return True

def someFunc():
    global args
    args.Max = 32
    num1 = NUM()
    for i in range(10000):
        add(num1, i)
    args.Max = 512
    # print(has(num1))

def symFunc():
    sym = adds(SYM(), ["a","a","a","a","b","b","c"])
    print(query.mid(sym), round(query.div(sym), 2))
    return 1.38 == round(query.div(sym), 2)

def numFunc():
    num1, num2 = NUM(), NUM()
    for i in range(10000):
        add(num1, rand())
    for i in range(10000):
        add(num2, rand() ** 2)
    print(1, round(query.mid(num1), 2), round(query.div(num1), 2))
    print(2, round(query.mid(num2), 2), round(query.div(num2), 2))
    return .5 == round(query.mid(num1), 1) and query.mid(num1)> query.mid(num2)

def crashFunc():
    num = NUM()
    return not hasattr(num, 'some.missing.nested.field')

def getCliArgs():
    global args
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-b", "--bins", type=int, default=16, required=False, help="initial number of bins")
    parser.add_argument("-d", "--d", type=float, default=0.35, required=False, help="different is over sd*d")
    parser.add_argument("-g", "--go", type=str, default="all", required=False, help="start-up action")
    parser.add_argument("-h", "--help", action='store_true', help="show help")
    parser.add_argument("-s", "--seed", type=int, default=937162211, required=False, help="random number seed")
    parser.add_argument("-f", "--file", type=str, default="../../etc/data/auto93.csv", required=False, help="data file")
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

def dataFunc():

    script_dir = os.path.dirname(__file__)
    full_path = os.path.join(script_dir, args.file)
    data = DATA(full_path)
    col = data.cols.x[1].col
    print(col.lo,col.hi, query.mid(col), query.div(col))
    print(query.stats(data))

def cloneFunc():

    script_dir = os.path.dirname(__file__)
    full_path = os.path.join(script_dir, args.file)
    data1 = DATA(full_path)
    data2 = DATA(data1, data1.rows)
    print(query.stats(data1))
    print(query.stats(data2))

def swayFunc():

    script_dir = os.path.dirname(__file__)
    full_path = os.path.join(script_dir, args.file)
    data = DATA(full_path)
    best, rest, _ = opt.sway(data)
    print("\nall ", query.stats(data))
    print("    ",   query.stats(data, query.div))
    print("\nbest", query.stats(best))
    print("    ",   query.stats(best, query.div))
    print("\nrest", query.stats(rest))
    print("    ",   query.stats(rest, query.div))
    print("\nall ~= best?", misc.diffs(best.cols.y, data.cols.y))
    print("best ~= rest?", misc.diffs(best.cols.y, rest.cols.y))

def halfFunc():

    script_dir = os.path.dirname(__file__)
    full_path = os.path.join(script_dir, args.file)
    data = DATA(full_path)
    left, right, A, B, c, _ = cluster.half(data)
    print(len(left), len(right))
    l, r = DATA(data, left), DATA(data, right)
    print("l", query.stats(l))
    print("r", query.stats(r))

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

def distFunc():

    script_dir = os.path.dirname(__file__)
    full_path = os.path.join(script_dir, args.file)
    data = DATA(full_path)
    num  = NUM()
    for row in data.rows:
        add(num, query.dist(data, row, data.rows[0]))
    print({"lo": num.lo, "hi": num.hi, "mid": round(query.mid(num)), "div": round(query.div(num))})

def treeFunc():

    script_dir = os.path.dirname(__file__)
    full_path = os.path.join(script_dir, args.file)
    data = DATA(full_path)
    cluster.showTree(cluster.tree(data))

def binsFunc():

    script_dir = os.path.dirname(__file__)
    full_path = os.path.join(script_dir, args.file)
    data = DATA(full_path)
    best, rest, _ = opt.sway(data)
    b4 = None
    print("all","","","", "{best= " + str(len(best.rows)) + ", rest= " + str(len(rest.rows)) + "}")
    result = disc.bins(data.cols.x, {"best": best.rows, "rest": rest.rows})
    for t in result:
        for range in t:
            if range.txt != b4:
                print("")
            b4 = range.txt
            print(range.txt,
                  range.lo,
                  range.hi,
                  round(query.value(range.y.has, len(best.rows), len(rest.rows), "best")),
                  range.y.has)

def explnFunc():
    script_dir = os.path.dirname(__file__)
    full_path = os.path.join(script_dir, args.file)
    data = DATA(full_path)
    best, rest, evals = opt.sway(data)
    rule, _ = disc.xpln(data, best, rest)
    print("\n-----------\nexplain=", disc.showRule(rule))
    data1 = DATA(data, disc.selects(rule, data.rows))
    print("all                ", query.stats(data), query.stats(data, query.div))
    print(f"sway with   {evals} evals", query.stats(best), query.stats(best, query.div))
    print(f"xpln on     {evals} evals", query.stats(data1), query.stats(data1, query.div))
    top, _ = query.betters(data, len(best.rows))
    top = DATA(data, top)
    print(f"sort with {len(data.rows)} evals", query.stats(top), query.stats(top, query.div))
