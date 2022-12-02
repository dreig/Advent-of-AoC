#!/usr/bin/env python
import re
from sys import stdin

data = [line.strip() for line in stdin.readlines()]

#   R, P, S
# R
# P
# S
# result (for $row) when $row plays against $column
OUTCOME = [
    [3, 0, 6],
    [6, 3, 0],
    [0, 6, 3],
]

TARGET_SCORE = {
    "X": 0,
    "Y": 3,
    "Z": 6,
}

def p1(data):
    score = 0
    for line in data:
        a,x = line.split()
        row = "XYZ".index(x)
        col = "ABC".index(a)
        score += OUTCOME[row][col] + row + 1

    return score


def p2(data):
    score = 0
    for line in data:
        a,x = line.split()
        target = TARGET_SCORE[x]
        col = "ABC".index(a)
        for row in range(3):
            if OUTCOME[row][col] == target:
                score += target + row + 1
                break

    return score



if __name__ == '__main__':
   print(p1(data))
   print(p2(data))
