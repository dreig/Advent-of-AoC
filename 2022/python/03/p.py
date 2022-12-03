#!/usr/bin/env python
from sys import stdin
import string
data = [line.strip() for line in stdin.readlines()]

def get_score(el):
    if el in string.ascii_lowercase:
        return string.ascii_lowercase.index(el)+1
    else:
        return string.ascii_uppercase.index(el)+27

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
    for group in zip(data[::3], data[1::3], data[2::3]):
        a,b,c = map(set, group)

        el = list(a & b & c)[0]
        res += get_score(el)

    return res


if __name__ == '__main__':
    print(p1(data))
    print(p2(data))
