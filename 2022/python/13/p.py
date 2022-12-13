#!/usr/bin/env python
from sys import stdin
import json
from functools import cmp_to_key

pairs = [pair.strip().split("\n") for pair in stdin.read().split("\n\n")]

LT = -1
EQ = 0
GT = 1

cmp_int = lambda l,r: LT if l < r else GT if l > r else EQ

def compare(lhs, rhs):
    if type(lhs) == int and type(rhs) == int:
        return cmp_int(lhs, rhs)
    elif type(lhs) == int:
        lhs = [lhs]
    elif type(rhs) == int:
        rhs = [rhs]

    for a,b in zip(lhs, rhs):
        if (res := compare(a,b)) != EQ:
            return res

    return cmp_int(len(lhs), len(rhs))

def parse_line(line):
    return json.loads(line)

def p1(pairs):
    answer = 0
    for i, pair in enumerate(pairs, 1):
        lhs, rhs = [parse_line(line) for line in pair]
        res = compare(lhs, rhs)
        if res == LT:
            answer += i

    return answer

def p2(pairs):
    sigA = [[2]]
    sigB = [[6]]
    lines = [sigA, sigB]
    for pair in pairs:
        lines.extend(map(parse_line, pair))

    s = sorted(lines, key=cmp_to_key(compare))
    answer = 1
    for i, line in enumerate(s, 1):
        if line == sigA or line == sigB:
            answer *= i

    return answer

if __name__ == '__main__':
   print(p1(pairs))
   print(p2(pairs))
