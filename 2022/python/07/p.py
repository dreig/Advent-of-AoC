#!/usr/bin/env python
from sys import stdin

data = [line.strip() for line in stdin.readlines()]

def process(data):
    processed = []
    sizes = []

    # for simplicity, this assumes that we don't visit the same directory more than once.
    for line in data:
        x,y,*rest = line.split()
        if x == "$":
            if y == "ls": continue
            if y == "cd":
                loc = rest[0]
                if loc == "..":
                    sz = sizes.pop()
                    processed.append(sz)
                    sizes[-1] += sz
                else:
                    sizes.append(0)
        elif x == "dir": continue
        else:
            sizes[-1] += int(x)

    while sizes:
        sz = sizes.pop()
        processed.append(sz)
        if sizes:
            sizes[-1] += sz

    return sorted(processed)

if __name__ == '__main__':
    sizes = process(data)

    p1_answer = sum(sz for sz in sizes if sz < 10**5)
    print(f"part1 = {p1_answer}")

    used = sizes[-1]
    to_free = max(used - 4*10**7, 0)
    print(f"used = {used}, to_free = {to_free}")
    for sz in sizes:
        if sz >= to_free:
            print(f"part2 = {sz}")
            break

