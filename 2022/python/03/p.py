#!/usr/bin/env python
from sys import stdin
import string
data = [line.strip() for line in stdin.readlines()]

def get_score(el):
    return string.ascii_letters.index(el)+1

def p1(data):
    res = 0
    for line in data:
        l = len(line) // 2
        left = set(line[:l])
        right = set(line[l:])

        el = list(left & right)[0]
        res += get_score(el)

    return res

def p2(data):
    res = 0
    for i in range(0, len(data), 3):
        a,b,c = map(set, data[i:i+3])

        el = list(a & b & c)[0]
        res += get_score(el)

    return res


if __name__ == '__main__':
    print(p1(data))
    print(p2(data))
