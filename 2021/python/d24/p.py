#!/usr/bin/env python
from sys import stdin
import functions

# data = [line.strip() for line in stdin.readlines()]

# def compare_blocks(b1, b2):
#     for i, (a,b) in enumerate(zip(b1, b2),1):
#         if a != b:
#             print(f"-{i}: {a}")
#             print(f"+{i}: {b}")
#     print('-' * 60)

# def p1(data):
#     blocks = []
#     cur_block = []
#     for line in data:
#         command, *args = line.split()
#         if command == "inp":
#             if cur_block: blocks.append(cur_block)
#             cur_block = []
#         else:
#             cur_block.append((command, *args))

#     if cur_block: blocks.append(cur_block)
#     return blocks

BLOCKS = [
    functions.block0,
    functions.block1,
    functions.block2,
    functions.block3,
    functions.block4,
    functions.block5,
    functions.block6,
    functions.block7,
    functions.block8,
    functions.block9,
    functions.block10,
    functions.block11,
    functions.block12,
    functions.block13,
]

RESULTS = [set() for _ in range(14)]

def preprocess():
    s = set([0])
    for (i,b) in enumerate(BLOCKS[:-1]):
        ns = set()
        for w in range(1,10):
            for z in s:
                res = b(w, z)
                # mn = mn if mn and mn < res else res
                # mx = mx if mx and mx > res else res
                ns.add(res)
        print(i, len(ns))
        s = ns
        RESULTS[i] = s

    RESULTS[-1] = targets = set([0])
    for i in range(12,-1,-1):
        b = BLOCKS[i+1]
        domain = set()
        for z in RESULTS[i]:
            for w in range(1, 10):
                res = b(w,z)
                if res in targets:
                    domain.add(z)
                    break
        RESULTS[i] = domain
        targets = domain

def solve(desired="largest"):
    rng = range(9, 0, -1) if desired == "largest" else range(1,10)
    answer = 0
    s = set([0])
    for i, b in enumerate(BLOCKS):
        ns = set()
        for w in rng:
            for z in s:
                res = b(w, z)
                if res in RESULTS[i]:
                    ns.add(res)
            if ns:
                answer = answer * 10 + w
                s = ns
                break

    return answer

if __name__ == '__main__':
    preprocess()

    largest = solve(desired="largest")
    print(f"largest MONAD = {largest}")
    # "largest" => 94399898949959

    smallest = solve(desired="smallest")
    print(f"smallest MONAD = {smallest}")
    # "smallest" => 21176121611511
