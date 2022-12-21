#!/usr/bin/env python
from sys import stdin
from itertools import chain
import operator

data = [line.strip().split(": ") for line in stdin.readlines()]

OPERATORS = {
    "+": operator.add,
    "*": operator.mul,
    "-": operator.sub,
    "/": operator.floordiv,
}

def p1(data):
    m = len(data)
    monkeys = { d[0]: n for d,n in zip(data, range(m)) }
    monkey_codes = { n: d[0] for d,n in zip(data, range(m)) }
    value = [None for _ in range(m)]
    deps = [([], []) for _ in range(m)]
    reqs = [0 for _ in range(m)]
    vis = [False for _ in range(m)]

    rootId = None
    for mc, ops in data:
        mid = monkeys[mc]
        if mc == "root": rootId = mid
        ops = ops.split()
        if len(ops) == 1:
            value[mid] = int(ops[0])
        else:
            op = OPERATORS[ops[1]]
            m0 = monkeys[ops[0]]
            m1 = monkeys[ops[2]]
            value[mid] = (op, m0, m1)
            deps[m0][0].append(mid)
            deps[m1][1].append(mid)
            reqs[mid] = 2

    q = []
    for mid in range(m):
        if reqs[mid] == 0:
            q.append(mid)

    while q:
        mid = q[0]
        q = q[1:]
        if vis[mid]: continue
        vis[mid] = True
        for m0 in deps[mid][0]:
            reqs[m0] -= 1
        for m1 in deps[mid][1]:
            reqs[m1] -= 1
        for nxt_mid in chain(*deps[mid]):
            if reqs[nxt_mid] == 0 and not vis[nxt_mid]:
                if type(value[nxt_mid]) == tuple:
                    op, m0, m1 = value[nxt_mid]
                    value[nxt_mid] = op(value[m0], value[m1])
                q.append(nxt_mid)

    return value[rootId]

def p2(data):
    m = len(data)
    monkeys = { d[0]: n for d,n in zip(data, range(m)) }
    monkey_codes = { n: d[0] for d,n in zip(data, range(m)) }
    value = [None for _ in range(m)]
    deps = [([], []) for _ in range(m)]
    reqs = [0 for _ in range(m)]
    vis = [False for _ in range(m)]

    rootId = None
    humnId = None
    for mc, ops in data:
        mid = monkeys[mc]
        ops = ops.split()
        if len(ops) == 1:
            value[mid] = int(ops[0])
        else:
            # op = OPERATORS[ops[1]]
            m0 = monkeys[ops[0]]
            m1 = monkeys[ops[2]]
            op = "==" if mc == "root" else ops[1]
            value[mid] = (op, m0, m1)

            deps[m0][0].append(mid)
            deps[m1][1].append(mid)
            reqs[mid] = 2

        if mc == "root":
            rootId = mid

        if mc == "humn":
            humnId = mid
            reqs[mid] = 1

    q = []
    for mid in range(m):
        if reqs[mid] == 0:
            q.append(mid)

    while q:
        mid = q[0]
        q = q[1:]
        if vis[mid]: continue
        vis[mid] = True
        for m0 in deps[mid][0]:
            reqs[m0] -= 1
        for m1 in deps[mid][1]:
            reqs[m1] -= 1
        for nxt_mid in chain(*deps[mid]):
            if reqs[nxt_mid] == 0 and not vis[nxt_mid]:
                if type(value[nxt_mid]) == tuple:
                    op, m0, m1 = value[nxt_mid]
                    op = OPERATORS[op]
                    value[nxt_mid] = op(value[m0], value[m1])
                q.append(nxt_mid)

    value[humnId] = "X"
    q = [humnId]
    while q:
        mid = q[0]
        q = q[1:]
        if vis[mid]: continue
        vis[mid] = True
        for m0 in deps[mid][0]: reqs[m0] -= 1
        for m1 in deps[mid][1]: reqs[m1] -= 1
        for nxt_mid in chain(*deps[mid]):
            if reqs[nxt_mid] == 0 and not vis[nxt_mid]:
                if type(value[nxt_mid]) == tuple:
                    op, m0, m1 = value[nxt_mid]
                    if type(m0) == int: m0 = value[m0]
                    if type(m1) == int: m1 = value[m1]
                    value[nxt_mid] = f"({m0} {op} {m1})"
                q.append(nxt_mid)

    return value[rootId]

if __name__ == '__main__':
    print(p1(data))
    print(p2(data))
