#!/usr/bin/env python
from sys import stdin, argv
from itertools import chain, cycle, count

instructions =  stdin.read().strip()

def is_valid(shape, well, h):
    return not any(s & w for s,w in zip(shape, well[h:]))

def move_right(shape, well, h):
    nxt_shape = list(n >> 1 for n in shape)
    if is_valid(nxt_shape, well, h):
        shape = nxt_shape

    return shape, well

def move_left(shape, well, h):
    nxt_shape = list(n << 1 for n in shape)
    if is_valid(nxt_shape, well, h):
        shape = nxt_shape

    return shape, well

def move_down(shape, well, h):
    return h and is_valid(shape, well, h-1)

shape_h_line = (0b000111100,)
shape_star = (
    0b000010000,
    0b000111000,
    0b000010000,
)
shape_corner = (
    0b000111000,
    0b000001000,
    0b000001000,
)
shape_v_line = (
    0b000100000,
    0b000100000,
    0b000100000,
    0b000100000,
)
shape_square = (
    0b000110000,
    0b000110000,
)

_level      = 0b100000001
_floor      = 0b111111111
_h_checker  = 0b011111110

SHAPES = [shape_h_line, shape_star, shape_corner, shape_v_line, shape_square]

INSTRUCTION = {
    ">": move_right,
    "<": move_left,
}

def find_height(well):
    h = len(well) -1
    while not well[h] & _h_checker:
        h -= 1
    return h

def print_well(well):
    print("\n".join(f"{n:0>9b}" for n in list(well)[::-1]))

def shortest_prefix(s):
    n = len(s)
    zz = [0] * n
    x,y = 0,1
    for i in range(1,n):
        z = min(zz[i-x], y-i) if i < y else 0
        while i + z < n and s[i+z] == s[z]: z += 1
        zz[i] = z
        if i+z > y:
            x,y = i,i+z
        if i+z == n:
            return i

    return -1

# TODO: clean this.
def p1(instructions, limit=10):
    ll = 40000
    well = [_floor] + [_level] * 3

    instructions = cycle(instructions)
    prev = 0
    cur_h = 0
    increments = []
    levels = []

    for n, shape in enumerate(cycle(SHAPES),1):
        if n > ll: break

        while cur_h + 1 + 3 + len(shape) > len(well):
            well.append(_level)

        h = cur_h + 4
        while True:
            ins = next(instructions)
            fun = INSTRUCTION[ins]
            shape, well = fun(shape, well, h)

            if move_down(shape, well, h):
                h -= 1
            else:
                # fix shape in place
                for row, i in zip(shape, count(h)):
                    well[i] = well[i] | row
                break

        cur_h = find_height(well)
        increments.append(cur_h - prev)
        levels.append(cur_h)
        prev = cur_h

    skip = 1000
    period = shortest_prefix(increments[skip:])
    print(period)
    period_sum = sum(increments[skip:skip+period])
    periods, rem = divmod(limit - skip, period)
    answer = sum(increments[:skip]) + period_sum * periods + sum(increments[skip:skip+rem])
    return answer

if __name__ == '__main__':
    print(f"linstructions = {len(instructions)}")
    limit = int(argv[1])
    print(f"limit={limit}")
    answer = p1(instructions, limit)
    print(f"answer={answer}")
