#!/usr/bin/env python
from sys import stdin

data = [line.strip() for line in stdin.readlines()]

DYX = [(0,1),(1,0),(-1,0),(0,-1)]

def solve(data):
    n = len(data)
    m = len(data[0])
    sy,sx = 0,0
    ey,ex = 0,0
    bd = [[0 for _ in range(m)] for _ in range(n)]

    for i,row in enumerate(data):
        for j,c in enumerate(row):
            if c == "S":
                sy,sx = i,j
                c = "a"
            elif c == "E":
                ey,ex = i,j
                c = "z"

            bd[i][j] = ord(c) - ord("a")

    inf = (n+m)**2;
    dist = [[inf for _ in range(m)] for _ in range(n)]
    dist[ey][ex] = 0
    q = [(ey,ex)]

    while q:
        (y,x) = q[0]
        q = q[1:]
        for dy,dx in DYX:
            ny,nx = y+dy,x+dx
            if 0 <= ny < n and 0 <= nx < m and bd[ny][nx] >= bd[y][x] - 1:
                if dist[ny][nx] > dist[y][x] + 1:
                    dist[ny][nx] = dist[y][x] + 1
                    q.append((ny,nx))


    p1 = dist[sy][sx] if dist[sy][sx] != inf else -1
    p2 = p1
    for i in range(n):
        for j in range(m):
            if bd[i][j] == 0 and dist[i][j] < p2:
                p2 = dist[i][j]

    return p1, p2

if __name__ == '__main__':
   print(solve(data))
