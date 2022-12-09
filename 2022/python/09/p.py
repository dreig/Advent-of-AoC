#!/usr/bin/env python
from sys import stdin

data = [line.strip().split() for line in stdin.readlines()]

DXY = {
    "R": (1,0),
    "U": (0,1),
    "L": (-1,0),
    "D": (0,-1),
}

def solve(data, rlength=2):
    positions = set()
    rope = [(0,0) for _ in range(rlength)]

    direction = lambda x: 1 if x > 0 else -1 if x < 0 else 0
    # the next node in the rope
    def catchup(head, tail):
        hx,hy = head
        tx,ty = tail
        dx,dy = hx - tx, hy -ty

        dirx, dx = direction(dx), abs(dx)
        diry, dy = direction(dy), abs(dy)

        if dx == 0:
            ty += diry * (dy > 1)
        elif dy == 0:
            tx += dirx * (dx > 1)
        elif dx > 1 or dy > 1:
            tx += dirx
            ty += diry

        return (tx, ty)

    for dir, cnt in data:
        dx,dy = DXY[dir]
        for _ in range(int(cnt)):
            head = rope[0]
            rope[0] = (head[0]+dx, head[1]+dy)

            for i in range(rlength-1):
                head, tail = rope[i:i+2]
                ntail = catchup(head, tail)
                if ntail == tail:
                    break

                rope[i+1] = ntail

            positions.add(rope[-1])

    return len(positions)

if __name__ == '__main__':
    print(solve(data, rlength=2))
    print(solve(data, rlength=10))
