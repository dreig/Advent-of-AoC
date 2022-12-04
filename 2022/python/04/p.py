#!/usr/bin/env python
from sys import stdin

data = [line.strip() for line in stdin.readlines()]

def p1(data):
    res = 0
    for line in data:
        l, r = line.split(",")
        la, lb = map(int, l.split("-"))
        ra, rb = map(int, r.split("-"))
        if (la <= ra and rb <= lb) or (ra <= la and lb <= rb):
            res+=1

    return res

def p2(data):
    res = 0
    for line in data:
        l, r = line.split(",")
        la, lb = map(int, l.split("-"))
        ra, rb = map(int, r.split("-"))
        if la <= rb and ra <= lb:
            res += 1
    return res

if __name__ == '__main__':
   print(p1(data))
   print(p2(data))
