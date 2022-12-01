#!/usr/bin/env python
from sys import stdin
from itertools import groupby

data = [line.strip() for line in stdin.readlines()]

def deer(data):
    groups = groupby(data, key=lambda x: x.isdigit())
    return [sum(map(int, cargo)) for (present, cargo) in groups if present]

def p1(dd):
    return max(dd)

def p2(dd):
    return sum(sorted(dd, reverse=True)[:3])

if __name__ == '__main__':
    dd = deer(data)

    print(p1(dd))
    print(p2(dd))
