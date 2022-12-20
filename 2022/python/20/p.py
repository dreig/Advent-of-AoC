#!/usr/bin/env python
from sys import stdin
# from itertools import repeat

data = [int(line.strip()) for line in stdin.readlines()]

def rotate(data, k=1):
    n = len(data)
    data = list(zip(data, range(n)))

    for _ in range(k):
        for i in range(n):
            for j in range(n):
                if data[j][1] != i: continue

                c = data[j][0]
                newpos = (j+c) % (n-1)
                if newpos == 0: newpos = n-1
                if newpos >= j:
                    data = data[:j] + data[j+1:newpos+1] + [data[j]] + data[newpos+1:]
                else:
                    data = data[:newpos] + [data[j]] + data[newpos:j] + data[j+1:]

                break
    return [d[0] for d in data]

def p1(data):
    n = len(data)
    data = rotate(data, 1)
    zero = data.index(0)
    indices = [(zero + d)%n for d in [1000,2000,3000]]

    return sum(data[i] for i in indices)

KEY = 811589153
def p2(data):
    n = len(data)
    data = rotate([d * KEY for d in data], 10)
    zero = data.index(0)
    indices = [(zero + d)%n for d in [1000,2000,3000]]

    return sum(data[i] for i in indices)


if __name__ == '__main__':
    print(p1(data))
    print(p2(data))
