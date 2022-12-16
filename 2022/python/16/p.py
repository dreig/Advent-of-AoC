#!/usr/bin/env python
from sys import stdin

data = [line.strip() for line in stdin.readlines()]

def parse_data(data):
    valves = []
    for line in data:
        valve, nbrs = line.split("; ")
        _, vid, *_, rate = valve.split()
        rate = int(rate.split("=")[-1])
        nbrs = [nbr.rstrip(",") for nbr in  nbrs.split()[4:]]
        valves.append((vid, rate, nbrs))

    valves.sort(reverse=True, key=lambda x: x[1])
    n = len(valves)
    vids = dict(zip([v[0] for v in valves], range(n)))
    dist = [[(i != j) * n**3 for j in range(n)] for i in range(n)]
    for vid, _, nbrs in valves:
        i = vids[vid]
        for nbr_id in nbrs:
            nbr_id = vids[nbr_id]
            dist[i][nbr_id] = 1
            dist[nbr_id][i] = 1

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    rates = [v[1] for v in valves]
    return rates, dist, vids["AA"]

def p1(rates, dist, start):
    n = sum(r > 0 for r in rates)
    start_dist = dist[start][:n]
    rates = rates[:n]
    dist = [row[:n] for row in dist[:n]]

    minutes = 30
    mm = 2**(n)
    dp = [[[-1 for _ in range(mm)] for _ in range(n)] for _ in range(minutes+1)]
    for v, fst_move in enumerate(start_dist):
        if fst_move < minutes:
            dp[fst_move][v][0] = 0

    for minute in range(minutes):
        for v in range(n):
            for mask in range(mm):
                if dp[minute][v][mask] == -1: continue
                # if not (mask ^ (1 << v)):
                for nbr in range(n):
                    if v == nbr: continue
                    if mask & (1 << nbr): continue
                    road = dist[v][nbr]
                    if minute + road >= minutes: continue
                    dp[minute+road][nbr][mask] = max(dp[minute+road][nbr][mask],
                        dp[minute][v][mask])

                if mask & (1 << v): continue

                dp[minute+1][v][mask|(1 << v)] = max(dp[minute+1][v][mask|(1 << v)], dp[minute][v][mask] + (minutes-minute-1)*rates[v])

    answer = 0
    for minute in range(minutes):
        for v in range(n):
            for mask in range(mm):
                answer = max(answer, dp[minute][v][mask])

    return answer

def p2(rates, dist, start):
    n = sum(r > 0 for r in rates)
    start_dist = dist[start][:n]
    rates = rates[:n]
    dist = [row[:n] for row in dist[:n]]

    minutes = 26
    mm = 2**(n)
    dp = [[[-1 for _ in range(mm)] for _ in range(n)] for _ in range(minutes+1)]
    for v, fst_move in enumerate(start_dist):
        if fst_move < minutes:
            dp[fst_move][v][0] = 0

    for minute in range(minutes):
        for v in range(n):
            for mask in range(mm):
                if dp[minute][v][mask] == -1: continue
                # if not (mask ^ (1 << v)):
                for nbr in range(n):
                    if v == nbr: continue
                    if mask & (1 << nbr): continue
                    road = dist[v][nbr]
                    if minute + road >= minutes: continue
                    dp[minute+road][nbr][mask] = max(dp[minute+road][nbr][mask],
                        dp[minute][v][mask])

                if mask & (1 << v): continue

                dp[minute+1][v][mask|(1 << v)] = max(dp[minute+1][v][mask|(1 << v)], dp[minute][v][mask] + (minutes-minute-1)*rates[v])

    best = [0 for _ in range(mm)]
    for mask in range(mm):
        for minute in range(minutes):
            for v in range(n):
                best[mask] = max(best[mask], dp[minute][v][mask])

    answer = 0
    for mask in range(mm):
        x = best[mask]
        s = mm - 1 - mask
        complement = s
        y = 0
        while True:
            y = max(y, best[complement])
            if not complement: break
            complement = (complement - 1) & s

        answer = max(answer, x+y)

    return answer

if __name__ == '__main__':
    rates, dist, start = parse_data(data)

    part1 = p1(rates, dist, start)
    print(f"part1 = {part1}")
    part2 = p2(rates, dist, start)
    print(f"part2 = {part2}")
