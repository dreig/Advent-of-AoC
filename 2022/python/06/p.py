#!/usr/bin/env python
from sys import stdin

data = stdin.read().strip()

def p(data, size):
    for i in range(size, len(data)+1):
        if len(set(data[i-size:i])) == size:
            return i
    raise Exception("something's not right")

if __name__ == '__main__':
   print(p(data, 4))
   print(p(data, 14))
