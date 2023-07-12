#!/usr/bin/env python
from sys import stdin

data = [line.strip() for line in stdin.readlines()]

MAP = ".#"

def print_board(bd):
    for row in bd:
        print("".join(MAP[c & 1] for c in row))

NBRS = [(dy,dx) for dy in range(-1,2) for dx in range(-1,2) if dy or dx]

DIR_NBRS = [
    [(-1,-1),(-1,0),(-1,1)], # NORTH: NW, N, NE
    [(1,1),(1,0),(1,-1)],    # SOUTH: SE, S, SW
    [(1,-1),(0,-1),(-1,-1)], # WEST:  SW, W, NW
    [(-1,1),(0,1),(1,1)],    # EAST:  NE, E, SE
]


def p1(data):
    n = len(data)
    m = len(data[0])

    offset = max(n,m) + 11
    N = n + 2*offset
    M = m + 2*offset
    bd = [[0] * M for _ in range(N)]
    where_to = [[0] * M for _ in range(N)]
    desired_by = [[0] * M for _ in range(N)]

    xmin, ymin = offset, offset
    ymax = n + offset
    xmax = m + offset
    elves_cnt = 0

    for i in range(n):
        for j in range(m):
            if data[i][j] == '#':
                elves_cnt += 1
                bd[offset+i][offset+j] = 1


    rounds = 10
    current_dir = 0

    # bd[i][j] & 1 => elf presence
    # (bd[i][j] >> 1) & 1 => move or stay
    # (bd[i][j] >> 2) & 3 => desired direction to move to
    # (bd[i][j] >> 4) & 7 => number of elves who want to move here
    for _ in range(rounds):
        for i in range(ymin, ymax):
            for j in range(xmin, xmax):
                if not (bd[i][j] & 1): continue
                stay_in_place = True
                if any((bd[i+nbry][j+nbrx] & 1) for nbry,nbrx in NBRS):
                    for d in range(current_dir,current_dir+4):
                        d = d & 3
                        if any(bd[i+dy][j+dx] & 1 for dy,dx in DIR_NBRS[d]):
                            continue
                        else:
                            stay_in_place = False
                            bd[i][j] |= 0b10 # move
                            bd[i][j] = (bd[i][j] | 0b1100) ^ 0b1100 # clear bits
                            bd[i][j] |= d << 2

                            dy,dx = DIR_NBRS[d][1]
                            bd[i+dy][j+dx] += 16
                            break

                if stay_in_place:
                    bd[i][j] += 16

                bd[i][j] = (bd[i][j] | 1) ^ 1 # clear bit

        for i in range(ymin, ymax):
            for j in range(xmin, xmax):
                if (bd[i][j] >> 1) & 1:
                    d = (bd[i][j] >> 2) & 3
                    dy,dx = DIR_NBRS[d][1]
                    desired_by = (bd[i+dy][j+dx] >> 4) & 7
                    if desired_by == 0:
                        print_board(bd[i-3:i+4][j-3][j+4])
                        raise Exception(f"at i={i}, j={j}")

                    elif desired_by == 1:


        # TODO: update ymin,ymax,xmin,xmax

        # clear the board.
        for i in range(ymin, ymax):
            for j in range(xmin, xmax):
                bd[i][j] &= 1

        current_dir = (current_dir + 1) & 3

    print(f"y=[{ymin}, {ymax}); x=[{xmin}, {xmax})")
    return (ymax -ymin) * (xmax - xmin) - elves_cnt

if __name__ == '__main__':
    p1(data)
