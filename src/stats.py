import json
import math
from num import NUM
from update import *
import query as query
import cluster as cluster
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
    Seed = util.args.seed
    low, high = low or 0, high or 1
    Seed = (16807 * Seed) % 2147483647
    return low + (high - low) * Seed / 2147483647

def eg(key, string, fun):
    global egs
    global help
    egs[key] = fun
    help += f"  -g {key}    {string}"

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
