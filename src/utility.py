import argparse
import csv
import json
import math
import os
from num import NUM
from data import DATA
from update import *
import query as query
import cluster as cluster
import Optimization as opt
import Discretization as disc
import random

args = None
Seed = None
n = 0
egs = {}

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

def getCliArgs(seed):
    global args
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-b", "--bins", type=int, default=16, required=False, help="initial number of bins")
    parser.add_argument("-d", "--d", type=float, default=0.35, required=False, help="different is over sd*d")
    parser.add_argument("-g", "--go", type=str, default="all", required=False, help="start-up action")
    parser.add_argument("-h", "--help", action='store_true', help="show help")
    parser.add_argument("-s", "--seed", type=int, default=seed, required=False, help="random number seed")
    parser.add_argument("-f", "--file", type=str, default="../etc/data/healthCloseIsses12mths0001-hard.csv", required=False, help="data file")
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

def explnFunc():
    global Seed
    Seed = util.args.seed
    val = {}
    script_dir = os.path.dirname(__file__)
    full_path = os.path.join(script_dir, args.file)
    data = DATA(full_path)
    best, rest, evals = opt.sway("sway1", data)
    val['all'] = query.stats(data)
    val["sway1"] = query.stats(best)
    rule, _ = disc.xpln(data, best, rest)
    data1 = DATA(data, disc.selects(rule, data.rows))
    val['xpln1'] = query.stats(data1)
    top, _ = query.betters(data, 1)
    top = DATA(data, top)
    val['top'] = query.stats(top)
    Seed = util.args.seed
    script_dir = os.path.dirname(__file__)
    full_path = os.path.join(script_dir, args.file)
    data = DATA(full_path)
    best, rest, evals = opt.sway("sway2", data)
    val["sway2"] = query.stats(best)
    rule, _ = disc.xpln2(data, best, rest)
    data1 = DATA(data, disc.selects2(rule, data.rows))
    val['xpln2'] = query.stats(data1)
    return val

