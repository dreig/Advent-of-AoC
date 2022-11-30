#!/usr/bin/env python
import sys
from functools import reduce
import operator
data = [[(1 if c == '1' else 0) for c in line.strip()] for line in sys.stdin.readlines()]

def bin2dec(binary):
    return reduce(lambda bin, x: 2*bin+ x, binary)

def p1(data):
    total = len(data)
    acc = [0] * len(data[0])
    for line in data:
        acc = [x + (bit == 1) for (x,bit) in zip(acc, line)]

    gamma = bin2dec((int(2*x >= total) for x in acc))
    epsilon = bin2dec((int(2*x < total) for x in acc))

    return gamma * epsilon

def reducer(data, key="most"):
    op = operator.ge if key == "most" else operator.lt
    bit = 0
    while len(data) > 1:
        if bit >= len(data[0]):
            print(bit, data[0], len(data))
            raise Exception("non unique answer")

        zero, one = [], []
        for line in data:
            if line[bit]:
                one.append(line)
            else:
                zero.append(line)

        data = one if op(len(one), len(zero)) else zero
        bit += 1

    return data[0]

def p2(data):
    oxygen = reducer(data, "most")
    scrubber = reducer(data, "least")

    oxygen = bin2dec(oxygen)
    scrubber = bin2dec(scrubber)
    print(f"oxygen={oxygen}; scrubber={scrubber}")
    return oxygen * scrubber

if __name__ == '__main__':
   print(p1(data))
   print(p2(data))
