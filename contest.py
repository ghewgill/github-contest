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

def flatten(a):
    r = []
    for x in a:
        if isinstance(x, list):
            r.extend(x)
        else:
            r.append(x)
    return r

def network(u):
    if not u in watching:
        watching[u] = set()
    return set(flatten(list(watchers[r]) for r in watching[u]))

def score(r, net):
    return 1.0 * len(watchers[r].intersection(net)) / len(net)

start = time.time()
results = open("results.txt", "w")
i = 0
for u in users:
    print i
    net = network(u)
    print "  net:", len(net)
    inter = set()
    for w in (watching[x] for x in net):
        inter.update(w)
    inter.difference_update(watching[u])
    print "  inter:", len(inter)
    best = sorted([x for x in [(score(r, net), r) for r in inter] if x[0] > 0], reverse=True)
    print "  best:", len(best)
    if len(best) == 0:
        best = [(0, 17)]
    print >>results, "%d:%s" % (u, ",".join(str(x[1]) for x in best[:10]))
    i += 1
    print "eta:", time.ctime(start + (time.time() - start) * len(users) / i)
results.close()
