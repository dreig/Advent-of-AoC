#!/usr/bin/env python
from sys import stdin
from collections import defaultdict

data = stdin.readline().strip()
data = data.removeprefix("target area:").strip()
target = [rng.strip().split("=")[1].split("..") for rng in data.split(",")]
targetX, targetY = [[int(coord) for coord in rng] for rng in target]

triang = lambda n: n * (n+1) // 2

def candidate_xs(targetX):
    mn, mx = targetX
    result = []
    for x in range(1, mx+1):
        if triang(x) < mn: continue
        if x > mx: break
        cur = []
        dist = 0
        for step,adv in zip(range(1,x+1), range(x, 0,-1)):
            dist += adv
            if mn <= dist <= mx:
                cur.append(step)

        if cur:
            result.append((x, cur))

    return result

def candidate_ys(targetY):
    mn, mx = targetY
    max_steps = max(abs(mn), abs(mx))
    result = defaultdict(lambda: [])
    for y in range(mn, abs(mn)+1):
        dist = 0
        pos_steps = 2*abs(y) + max_steps
        for step, adv in zip(range(1, pos_steps), range(y, 2*mn, -1)):
            dist += adv
            if mn <= dist <= mx:
                result[step].append(y)
            if dist < mn: break

    return result


def p2(targetX, targetY):
    xs = candidate_xs(targetX)
    ys = candidate_ys(targetY)

    mx = max(ys.keys())
    answer = set()
    for x, steps in xs:
        for s in steps:
            for y in ys.get(s, []):
                answer.add((x,y))

        if x == steps[-1]:
            for potential_steps in range(x+1, mx+1):
                for y in ys.get(potential_steps, []):
                    answer.add((x, y))

    return len(answer)

if __name__ == '__main__':
    answer = p2(targetX, targetY)
    print(answer)

