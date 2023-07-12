#!/usr/bin/env python
from sys import stdin

data = [line.strip() for line in stdin.readlines()]
def manhattan(a,b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def parse_data(data):
    def get_point(s):

        s = s.split("at ")[-1].strip()

        s = [cc.split("=")[-1] for cc in s.split(", ")]
        x,y = map(int, s)
        return (x,y)

    res = []
    for line in data:
        sensor, beacon = [get_point(seg) for seg in line.split(": ")]
        res.append((sensor, beacon))

    return res

def part1(pts, line = 10):
    segments = []
    beacons = set()
    for s, b in pts:
        dist = manhattan(s,b)
        to_line = abs(line - s[1])
        if to_line > dist:
            continue
        l = s[0] - (dist - to_line)
        r = s[0] + (dist - to_line)
        segments.append((l,r))
        if b[1] == line:
            beacons.add(b[0])

    segments.sort()
    # print("\n".join(map(str, segments)))
    cl, cr = segments[0]
    answer = 0
    for l, r in segments[1:]:
        if l <= cr:
            cr = max(r, cr)
        else:
            answer += cr - cl + 1
            cl, cr = l, r
    answer += cr - cl + 1

    return answer - len(beacons)

LIMIT = int(4e6)

def part2(pts, line):
    segments = []
    beacons = set()
    for s, b in pts:
        dist = manhattan(s,b)
        to_line = abs(line - s[1])
        if to_line > dist:
            continue
        l = s[0] - (dist - to_line)
        r = s[0] + (dist - to_line)
        l = max(l, 0)
        r = min(r, LIMIT)
        segments.append((l,r))
        if b[1] == line:
            beacons.add(b[0])

    segments.sort()
    # print("\n".join(map(str, segments)))
    cl, cr = segments[0]
    answer = 0
    x = -1
    for l, r in segments[1:]:
        if l <= cr:
            cr = max(r, cr)
        else:
            answer += cr - cl + 1
            if cr + 1 < l:
                x = cr+1
            cl, cr = l, r

    answer += cr - cl + 1

    if answer <= LIMIT:
        return x * LIMIT + y
    else:
        return -1

if __name__ == '__main__':
    points = parse_data(data)
    print(part1(points, 2000000))
    for y in range(0, LIMIT+1):
        freq = part2(points, y)
        if freq > 0:
            print(freq)
            break
