#!/usr/bin/env python
from sys import stdin
from math import lcm

data = [line.strip() for line in stdin.readlines()]

WALL = 0
EMPTY = 1
WIND_R = 2
WIND_L = 3
WIND_U = 4
WIND_D = 5

BD_CODE = {
    "#": WALL,
    ".": EMPTY,
    ">": WIND_R,
    "<": WIND_L,
    "^": WIND_U,
    "v": WIND_D,
}

BD_CHAR = "#.><^v"

INF = 10**8
DYX = [
    (0,0),  # STAY IN PLACE
    (0,1),  # R
    (1,0),  # D
    (0,-1), # L
    (-1,0), # U
]

def parse_board(data):
    bd = [[BD_CODE[c] for c in row] for row in data]

    return bd

def solve(data):
    bd = parse_board(data)
    n = len(bd)
    m = len(bd[0])
    period = lcm(n-2, m-2)

    dp = [[[[INF for _ in range(period)] for _ in range(m)] for _ in range(n)] for _ in range(3)]
    dp[0][0][1][0] = 0

    def is_pos_free(y, x, time):
        py = (y-1 - time) % (n-2) + 1
        if bd[py][x] == WIND_D:
            return False
        py = (y-1 + time) % (n-2) + 1
        if bd[py][x] == WIND_U:
            return False

        px = (x-1 - time) % (m-2) + 1
        if bd[y][px] == WIND_R:
            return False
        px = (x-1 + time) % (m-2) + 1
        if bd[y][px] == WIND_L:
            return False

        return True

    q = [(0,0,1,0)]
    while q:
        lvl, y, x, tt = q[0]
        q = q[1:]
        cost = dp[lvl][y][x][tt]
        if lvl == 0 and y == n-1 and x == m-2:
            lvl += 1
        if lvl == 1 and y == 0 and x == 1:
            lvl += 1
        for dy,dx in DYX:
            ny,nx = y+dy,x+dx
            nt = (tt + 1) % period
            if 0 <= ny < n and 0 <= nx < m and bd[ny][nx] != WALL:
                if is_pos_free(ny, nx, nt) and dp[lvl][ny][nx][nt] > cost + 1:
                    dp[lvl][ny][nx][nt] = cost+1
                    q.append((lvl,ny,nx,nt))

    p1 = min(dp[0][-1][-2])
    p2 = min(dp[2][-1][-2])
    return p1, p2

if __name__ == '__main__':
    p1,p2 = solve(data)
    print(f"part1={p1}")
    print(f"part2={p2}")
