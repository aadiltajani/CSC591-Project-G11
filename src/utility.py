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

def delta(i, other): 
    e, y, z = 1E-32, i, other
    return abs(y.mu - z.mu) / (e + y.sd ** 2 / y.n + z.sd **2 / z.n) ** 0.5 

def samples(t, n = None): 
    u = []
    for i in range(n if n is not None else len(t)): 
        u.append(random.choice(t))
    return u

def add(i, x):
    i.n += 1
    d = x - i.mu
    i.mu = i.mu + d / i.n
    i.m2 = i.m2 + d * (x - i.mu)
    i.sd = 0 if i.n < 2 else (i.m2 / (i.n - 1)) ** 0.5

def cliffsDelta(ns1, ns2): 
    n, gt, lt = 0, 0, 0 
    if len(ns1) > 128: 
        ns1 = samples(ns1, 128)
    if len(ns2) > 128: 
        ns2 = samples(ns2, 128)
    for x in ns1:
        for y in ns2: 
            n = n + 1 
            if x > y: 
                gt += 1
            if x < y: 
                lt += 1
    return abs(lt - gt) / n <= 0.3

def bootstrap(y0, z0): 
    x, y, z, yhat, zhat = NUM(), NUM(), NUM(), [], []
    for y1 in y0:
        add(x, y1)
        add(y, y1)
    for z1 in z0:
        add(x, z1)
        add(z, z1)
    xmu, ymu, zmu = x.mu, y.mu, z.mu
    for y1 in y0: 
        yhat.append(y1 - ymu + xmu)
    for z1 in z0: 
        zhat.append(z1 - zmu + xmu)
    tobs = delta(y, z)
    n = 0
    for i in range(512):
        ys = NUM()
        zs = NUM()
        for y in samples(yhat):
            add(ys, y)
        for z in samples(zhat):
            add(zs, z)

        if delta(ys, zs) > tobs:
            n += 1
    print(n, n/512)
    return n / 512 >= 0.01

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

def RX(t, s = ""):
    return {"name":s, "rank":0, "n":len(t), "show":"", "has":sorted(t)}

def merge(rx1, rx2):
    rx3 = RX([], rx1['name'])
    rx3['has'] = rx1['has'] + rx2['has']
    rx3['has'] = sorted(rx3['has'])
    rx3['n'] = len(rx3['has'])
    return rx3

def mid(t):
    t= t['has'] if t['has'] else t
    n = (len(t)-1)//2
    return (t[n] +t[n+1])/2 if len(t)%2==0 else t[n+1]

def div(t):
    t= t['has'] if t['has'] else t
    return (t[ len(t)*9//10 ] - t[ len(t)*1//10 ])/2.56

def tiles(rxs):
  huge = float('inf')
  lo,hi = huge, float('-inf')
  for rx in rxs: 
    lo,hi = min(lo,rx['has'][0]), max(hi, rx['has'][len(rx['has'])-1])
  for rx in rxs:
    t,u = rx['has'],[]
    def of(x,most):
        return int(max(1, min(most, x)))
    
    def at(x):
        return t[of(len(t)*x//1, len(t))]

    def pos(x):
        return math.floor(of(40*(x-lo)/(hi-lo+1E-32)//1, 40))

    for i in range(41):
        u.append(" ")
    a,b,c,d,e= at(.1), at(.3), at(.5), at(.7), at(.9) 
    A,B,C,D,E= pos(a), pos(b), pos(c), pos(d), pos(e)
    for i in range(A,B+1):
        u[i]="-"
    for i in range(D,E+1):
        u[i]="-"
    u[40//2] = "|" 
    u[C] = "*"
    form = "%6.2f"
    rx["show"] = rx["show"] + ''.join(u) + "{" + form % a
    for x in [b, c, d, e]:
        rx["show"]= rx["show"] + ", " + form % x
    rx["show"] = rx["show"] + "}"
  return rxs

def scottKnot(rxs):
  def merges(i,j):
    out = RX([],rxs[i]['name'])
    for k in range(i, j+1):
        out = merge(out, rxs[j])
    return out
  
  def same(lo,cut,hi):
    l= merges(lo,cut)
    r= merges(cut+1,hi)
    return cliffsDelta(l['has'], r['has']) and bootstrap(l['has'], r['has'])
  
  def rxs_sort(rxs):
    for i, x in enumerate(rxs):
        for j, y in enumerate(rxs):
            if mid(x) < mid(y):
                rxs[j], rxs[i] = rxs[i], rxs[j]
    return rxs
    
  def recurse(lo,hi,rank):
    b4 = merges(lo,hi)
    best = 0
    cut = None
    for j in range(lo,hi+1):
      if j < hi:
        l   = merges(lo,  j)
        r   = merges(j+1, hi)
        now = (l['n']*(mid(l) - mid(b4))**2 + r['n']*(mid(r) - mid(b4))**2) / (l['n'] + r['n'])
        if now > best:
          if abs(mid(l) - mid(r)) >= cohen:
            cut, best = j, now
    if cut != None and not same(lo, cut, hi):
      rank = recurse(lo, cut, rank) + 1
      rank = recurse(cut+1, hi,  rank) 
    else:
      for i in range(lo, hi+1):
        rxs[i]['rank'] = rank
    return rank
  rxs = rxs_sort(rxs)
  cohen = div(merges(0,len(rxs)-1)) * 0.35
  recurse(0, len(rxs)-1, 1)
  return rxs
