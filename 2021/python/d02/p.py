#!/usr/bin/env python
import sys

data = [line.strip().split() for line in sys.stdin.readlines()]

def p1(data):
    x,y = 0,0
    for to, num in data:
        num = int(num)
        if to == "forward":
            x += num
        elif to == "up":
            y -= num
        elif to == "down":
            y += num
    return x*y

def p2(data):
    x, y, aim = 0,0, 0
    for to, num in data:
        num = int(num)
        if to == "forward":
            x += num
            y += aim * num
        elif to == "up":
            aim -= num
        elif to == "down":
            aim += num
    return x*y

if __name__ == '__main__':
   print(p1(data))
   print(p2(data))
