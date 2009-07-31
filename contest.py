# This code is Copyright (c) 2009 Greg Hewgill, All Rights Reserved.
# If you use it in your own contest submission, everybody will know.

import time

data = [tuple(map(int, x.strip().split(":"))) for x in open("download/data.txt").readlines()]
repos = set([int(x.strip().split(":")[0]) for x in open("download/repos.txt").readlines()])
users = [int(x) for x in open("download/test.txt").readlines()]

watchers = {}
watching = {}
for u, r in data:
    if r not in watchers:
        watchers[r] = set()
    watchers[r].add(u)
    if u not in watching:
        watching[u] = set()
    watching[u].add(r)

def avg(a):
    if len(a) == 0:
        return 0
    return sum(a) / len(a)

def flatten(a):
    r = []
    for x in a:
        if isinstance(x, list):
            r.extend(x)
        else:
            r.append(x)
    return r

def top(n, a):
    r = []
    for x in a:
        if len(r) == 0 or x > r[-1]:
            r = sorted(r + [x], reverse=True)[:n]
    return r

def network(u):
    return set(flatten(list(watchers[r]) for r in watching[u]))

def score(u, r, net):
    return len(watchers[r] & net)

start = time.time()
results = open("results.txt", "w")
popular = top(10, ((len(watchers[r]), r) for r in repos))
i = 0
for u in users:
    print i
    if u not in watching:
        watching[u] = set()
    net = network(u)
    print "  net:", len(net)
    inter = set(flatten(list(watching[x]) for x in net)) - watching[u]
    print "  inter:", len(inter)
    best = top(10, ((score(u, r, net), r) for r in inter - watching[u]))
    print "  best:", best
    best.extend(popular[:10-len(best)])
    print >>results, "%d:%s" % (u, ",".join(str(x[1]) for x in best))
    i += 1
    print "eta:", time.ctime(start + (time.time() - start) * len(users) / i)
results.close()
