#!/usr/bin/env python
from sys import stdin

data = [line.strip() for line in stdin.readlines()]

AIR = 0
ROCK = 1
SAND = 2
_out = lambda x: "." if x == AIR else "#" if x == ROCK else "o"

def parse_board(data):
    bd = [[AIR for _ in range(800)] for _ in range(200)]

    for line in data:
        prx, pry = None, None
        for coord in line.split(" -> "):
            x,y = (int(cc) for cc in coord.split(","))
            if prx == x and pry is not None:
                s,e = sorted([pry, y])
                for i in range(s,e+1):
                    bd[i][x] = ROCK
            elif pry == y and prx is not None:
                s,e = sorted([prx, x])
                for i in range(s,e+1):
                    bd[y][i] = ROCK

            prx,pry = x,y

    return bd

NXY = [(0,1), (-1,1), (1,1)]

def simulate(bd):
    SX,SY = 500,0
    n = len(bd)
    m = len(bd[0])
    cnt, done = 0, False
    while not done:
        x, y = SX, SY
        stopped = False

        while not stopped:
            stopped = True
            for dx,dy in NXY:
                nx, ny = x+dx, y+dy # next possible square
                if nx < 0 or nx >= m or ny >= n: # if outside the board
                    done = True
                    break

                if bd[ny][nx] == AIR: # if next position is available
                    stopped = False
                    x,y = nx,ny
                    break

        if done:
            return cnt

        bd[y][x] = SAND
        cnt += 1

        if bd[SY][SX] != AIR:
            return cnt

def p1(data):
    bd = parse_board(data)
    answer = simulate(bd)
    print(f"part1 = {answer}")

def p2(data):
    bd = parse_board(data)
    n, m = len(bd), len(bd[0])

    mxy = 0
    for y in range(n):
        if any(bd[y]):
            mxy = y

    n = mxy+3
    bd = bd[:n]
    for x in range(m):
        bd[-1][x] = ROCK

    answer = simulate(bd)
    print(f"part2 = {answer}")

def print_board(bd):
    for row in bd:
        print("".join(map(_out, row[280:800])))

if __name__ == '__main__':
    p1(data)
    p2(data)

