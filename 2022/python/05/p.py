#!/usr/bin/env python
from sys import stdin, argv

data = [line.strip() for line in stdin.readlines()]
INPUTS = {
    "sample": [
        "ZN",
        "MCD",
        "P"
    ],
    "input": [
        "CZNBMWQV",
        "HZRWCB",
        "FQRJ",
        "ZSWHFNMT",
        "GFWLNQP",
        "LPW",
        "VBDRGCQJ",
        "ZQNBW",
        "HLFCGTJ",
    ],
}

def read_tops(stacks):
    return "".join(stack[-1] for stack in stacks)

def p1(data, stacks):
    stacks = [list(stack) for stack in stacks]
    for line in data:
        _, cnt, _, frm, _, to = line.split()
        cnt = int(cnt)
        frm = int(frm) - 1
        to = int(to) - 1
        for _ in range(cnt, 0, -1):
            top = stacks[frm].pop()
            stacks[to].append(top)

    return read_tops(stacks)

def p2(data, stacks):
    stacks = [list(stack) for stack in stacks]
    for line in data:
        _, cnt, _, frm, _, to = line.split()
        cnt = int(cnt)
        frm = int(frm) - 1
        to = int(to) - 1

        top = stacks[frm][-cnt:]
        stacks[frm] = stacks[frm][:-cnt]
        stacks[to].extend(top)

    return read_tops(stacks)

if __name__ == '__main__':
    print(argv[1])
    stacks = INPUTS[argv[1]]
    print(p1(data, stacks))
    print(p2(data, stacks))
