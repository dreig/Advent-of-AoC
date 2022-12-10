#!/usr/bin/env python
from sys import stdin

data = [line.strip() for line in stdin.readlines()]

def p1(data):
    x = 1
    cycle = 1

    result = 0
    def strength(cycle, x):
        if cycle <= 220 and cycle % 40 == 20:
            return cycle * x
        return 0

    for line in data:
        result += strength(cycle, x)

        cycle += 1
        if line == "noop": continue

        dx = int(line.split()[1])
        result += strength(cycle, x)

        cycle += 1
        x += dx

    return result

def p2(data):
    x = 1
    cycle = 1
    N = 40

    board = [['.' for _ in range(N)] for _ in range(6)]
    def draw(cycle, x):
        row, col = divmod(cycle-1, N)
        symbol = "#" if x-1 <= col <= x+1 else "."

        return row, col, symbol

    for line in data:
        r,c, sym = draw(cycle, x)
        board[r][c] = sym

        cycle += 1
        if line == "noop": continue

        dx = int(line.split()[1])
        r,c, sym = draw(cycle, x)
        board[r][c] = sym

        cycle += 1
        x += dx

    return "\n".join("".join(row) for row in board)

if __name__ == '__main__':
    print(p1(data))

    print(p2(data))
