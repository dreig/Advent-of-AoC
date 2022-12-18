#!/usr/bin/env python
from sys import stdin

data = [line.strip() for line in stdin.readlines()]
points = [tuple(map(int, line.split(","))) for line in data]

def p1(points):
    n = len(points)
    answer = 6*n
    for i in range(n):
        for j in range(i+1, n):
            if sum(abs(a - b) for a, b in zip(points[i], points[j])) == 1:
                answer -= 2

    return answer

def p2(points):
    n = 22
    cube = [[[0 for _ in range(n)] for _ in range(n)] for _ in range(n)]
    points = [(a+1,b+1,c+1) for a,b,c in points]
    for a,b,c in points:
        cube[a][b][c] = 1

    for b in range(n):
        for c in range(n):
            if not cube[0][b][c]: cube[0][b][c] = 2
            if not cube[n-1][b][c]: cube[n-1][b][c] = 2
            if not cube[b][0][c]: cube[b][0][c] = 2
            if not cube[b][n-1][c]: cube[b][n-1][c] = 2
            if not cube[b][c][0]: cube[b][c][0] = 2
            if not cube[b][c][n-1]: cube[b][c][n-1] = 2

    dxyz = [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]

    for i in range(1, n):
        if i > n-i-1: break
        for b in range(n):
            for c in range(n):
                for a in [i, n-1-i]:
                    coords = [a,b,c]
                    for j in range(3):
                        coords[0],coords[j] = coords[j],coords[0]
                        x,y,z = coords
                        if cube[x][y][z] in (1,2): continue
                        for dx,dy,dz in dxyz:
                            nx = x+dx
                            ny = y+dy
                            nz = z+dz
                            if 0<=nx<n and 0<=ny<n and 0 <=nz<n:
                                if cube[nx][ny][nz] == 2:
                                    cube[x][y][z] = 2
                        coords[0],coords[j] = coords[j],coords[0]



    outside = 0
    for a in range(1, n-1):
        for b in range(1, n-1):
            for c in range(1, n-1):
                if cube[a][b][c] == 1:
                    for dx,dy,dz in dxyz:
                        nx = a+dx
                        ny = b+dy
                        nz = c+dz
                        if 0<=nx<n and 0<=ny<n and 0 <=nz<n:
                            if cube[nx][ny][nz] == 2:
                                outside += 1

    return outside


if __name__ == '__main__':
    print(p1(points))
    print(p2(points))
