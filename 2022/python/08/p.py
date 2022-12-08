#!/usr/bin/env python
from sys import stdin

data = [line.strip() for line in stdin.readlines()]
grid = [list(map(int, line)) for line in data]

def solve(grid):
    n = len(grid)
    m = len(grid[0])

    seen = [[0 for _ in range(m)] for _ in range(n)]
    prod = [[1 for _ in range(m)] for _ in range(n)]

    for i, row in enumerate(grid):
        mx = -1
        desc = []
        for j, val in enumerate(row):
            if val > mx:
                seen[i][j] = True
                mx = val

            while desc:
                pos, height = desc[-1]
                if height >= val:
                    break
                desc.pop()
            pos = desc[-1][0] if desc else 0
            prod[i][j] *= j - pos
            desc.append((j, val))

        mx = -1
        desc = []
        for j,val in reversed(list(enumerate(row))):
            if val > mx:
                seen[i][j] = True
                mx = val

            while desc:
                pos, height = desc[-1]
                if height >= val:
                    break
                desc.pop()
            pos = desc[-1][0] if desc else m-1
            prod[i][j] *= pos -j

            desc.append((j, val))

    trans = list(zip(*grid))
    for j, col in enumerate(trans):
        mx = -1
        desc = []
        for i, val in enumerate(col):
            if val > mx:
                seen[i][j] = True
                mx = val

            while desc:
                pos, height = desc[-1]
                if height >= val:
                    break
                desc.pop()
            pos = desc[-1][0] if desc else 0
            prod[i][j] *= i - pos

            desc.append((i, val))

        mx = -1
        desc = []
        for i,val in reversed(list(enumerate(col))):
            if val > mx:
                seen[i][j] = True
                mx = val

            while desc:
                pos, height = desc[-1]
                if height >= val:
                    break
                desc.pop()
            pos = desc[-1][0] if desc else n-1
            prod[i][j] *= pos - i
            desc.append((i, val))

    tot = sum(sum(row) for row in seen)
    mx = max(max(row) for row in prod)
    return(tot, mx)

if __name__ == '__main__':
   print(solve(grid))
