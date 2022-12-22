#!/usr/bin/env python
from sys import stdin

EMPTY = 0
SPACE = 1
WALL  = 2

TILES = {
    " ": EMPTY,
    ".": SPACE,
    "#": WALL,
}

board, instructions = stdin.read().split("\n\n")
def parse_board(bd):
    bd = bd.split("\n")
    n = len(bd)
    m = max(len(row) for row in bd)
    out = []
    rows = []
    for row in bd:
        l, r = -1, 0
        out_row = []
        for i,c in enumerate(row):
            out_row.append(TILES[c])
            if c == " ": continue
            if l == -1: l = i
            r = i
        out_row.extend(EMPTY for _ in range(m - len(out_row)))
        out.append(out_row)
        rows.append((l,r))
    cols = []
    for j in range(m):
        l, r = -1, 0
        for i in range(n):
            if out[i][j] == EMPTY: continue
            if l == -1: l = i
            r = i
        cols.append((l,r))

    return out, rows, cols

def parse_instructions(line):
    line = line.strip()
    cur = 0
    out = []
    for c in line:
        if c.isdigit():
            cur = cur * 10 + ord(c) - ord('0')
        else:
            if cur:
                out.append(cur)
                cur = 0
            out.append(c)
    if cur:
        out.append(cur)
        cur = 0

    return out

BD, rows, cols = parse_board(board)
instructions   = parse_instructions(instructions)


RIGHT = 0
DOWN  = 1
LEFT  = 2
UP    = 3

REVERSE_DIRECTION = [LEFT,UP,RIGHT,DOWN]

        # R      D       L      U
DIRS = [(0,1), (1,0), (0,-1), (-1, 0)]

def turn_right(dir_ind):
    return (dir_ind + 1) % 4
def turn_left(dir_ind):
    return (dir_ind + 3) % 4

def p1():
    y = 0
    x = rows[0][0]
    dir_ind = RIGHT
    direction = DIRS[dir_ind]

    for ins in instructions:
        if type(ins) == int:
            dy,dx = direction
            for _ in range(ins):
                ny, nx = y+dy, x+dx
                if dx:
                    l,r = rows[y]
                    if nx < l:
                        nx = r
                    elif nx > r:
                        nx = l
                else:
                    l,r = cols[x]
                    if ny < l:
                        ny = r
                    elif ny > r:
                        ny = l
                if BD[ny][nx] != WALL:
                    y,x = ny,nx
        elif ins == "L":
            dir_ind = turn_left(dir_ind)
        elif ins == "R":
            dir_ind = turn_right(dir_ind)
        direction = DIRS[dir_ind]

    return 1000 * (y+1) + 4 * (x+1) + dir_ind

# The coordinates of the upper-left corner of each of the six faces of the cube
# (represents my custom input)
CUBE = [
    (0,50),
    (0,100),
    (50,50),
    (100,50),
    (100,0),
    (150,0),
]

# The adjacency table of faces: (represents my custom input)
# If you leave old_face via old edge,
#   you enter (new_face, new_edge) = ADJ[old_face][old_edge]
ADJ = [
    [(1,LEFT), (2,UP), (4,LEFT), (5,LEFT)],
    [(3,RIGHT),(2,RIGHT),(0,RIGHT),(5,DOWN)],
    [(1,DOWN),(3,UP),(4,UP),(0,DOWN)],
    [(1,RIGHT),(5,RIGHT),(4,RIGHT),(2,DOWN)],
    [(3,LEFT),(5,UP),(0,LEFT),(2,LEFT)],
    [(3,DOWN),(1,UP),(0,UP),(4,DOWN)],
]

FACE_ENTRANCE = [49, 49, 0, 0]

def p2():
    faces = []
    for f in range(6):
        y0,x0 = CUBE[f]
        y1,x1 = y0+50,x0+50
        faces.append([row[x0:x1] for row in BD[y0:y1]])

    face = 0
    y,x = 0,0
    dir_ind = RIGHT
    direction = DIRS[dir_ind]
    for ins in instructions:
        if type(ins) == int:
            for _ in range(ins):
                dy, dx = direction
                ny, nx = y+dy, x+dx
                nface, ndir = face, dir_ind
                # If out of bounds, move to another face
                if ny < 0 or ny >= 50 or nx < 0 or nx >= 50:
                    nface, enter_edge = ADJ[face][dir_ind]

                    # This part dictates how the orientation changes depending on old_edge and new_edge.
                    if ny < 0 or ny >= 50:
                        ny = FACE_ENTRANCE[enter_edge]
                        if enter_edge == REVERSE_DIRECTION[dir_ind]:
                            pass
                        elif enter_edge == dir_ind:
                            nx = 49-nx
                        elif enter_edge == turn_left(dir_ind):
                            ny,nx = nx,ny
                        else:
                            ny,nx = 49-nx,ny

                    elif nx < 0 or nx >= 50:
                        nx = FACE_ENTRANCE[enter_edge]
                        if enter_edge == REVERSE_DIRECTION[dir_ind]:
                            pass
                        elif enter_edge == dir_ind:
                            ny = 49-ny
                        elif enter_edge == turn_right(dir_ind):
                            ny,nx = nx,ny
                        else:
                            ny,nx = 49-nx,ny

                    ndir = REVERSE_DIRECTION[enter_edge]

                if faces[nface][ny][nx] != WALL:
                    face = nface
                    dir_ind = ndir
                    direction = DIRS[dir_ind]
                    y,x = ny,nx

        elif ins == "L":
            dir_ind = turn_left(dir_ind)
            direction = DIRS[dir_ind]
        elif ins == "R":
            dir_ind = turn_right(dir_ind)
            direction = DIRS[dir_ind]

    base_y,base_x = CUBE[face]
    return 1000 * (base_y + y + 1) + 4 * (base_x +x+1) + dir_ind

if __name__ == '__main__':
    print(p1())
    print(p2())
