#!/usr/bin/env python
from sys import stdin

# data = [line.strip() for line in stdin.readlines()]

SNAFU_DIG = {
    "=": -2,
    "-": -1,
    "0": 0,
    "1": 1,
    "2": 2,
}


TXT = "=-012"

def snafu2dec(ss):
    num = 0
    for c in ss:
        num = num*5 + SNAFU_DIG[c]
    return num

def dec2penta(num):
    digits = []
    while num:
        num, rem = divmod(num, 5)
        digits.append(rem)
    return list(reversed(digits))

def dec2snafu(num):
    pw = 0
    a = 1
    cover = 2
    base = a*5**pw
    while base + cover < num:
        if a == 1:
            a += 1
            base = a*5**pw
        else:
            a = 1
            pw += 1
            base = a*5**pw
            cover = 5*cover + 2
    assert base - cover <= num <= base + cover

    return str(a) + "".join(TXT[d] for d in dec2penta(num + cover)[1:])

def p1(data):
    answer = sum(snafu2dec(ss) for ss in data)
    print(answer)

if __name__ == '__main__':
    # p1(data)
    for n in range(23):
        print(n, "\t", dec2snafu(n))

