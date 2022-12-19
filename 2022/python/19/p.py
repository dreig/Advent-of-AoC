#!/usr/bin/env python
from sys import stdin, argv

data = [line.strip() for line in stdin.readlines()]

def simulate(minutes, ore_cost, clay_cost, obs_cost, geode_cost):
    memo = {}
    max_ore_robots = max(ore_cost, clay_cost, obs_cost[0], geode_cost[0])
    max_clay_robots = obs_cost[1]
    max_obs_robots = geode_cost[1]
    def get(tpl):
        mn, ore, clay, obs, ore_rs, clay_rs, obs_rs = tpl
        if mn <= 1: return 0
        if ore >= geode_cost[0] and obs >= geode_cost[1]:
            enough_ore = ore_rs >= geode_cost[0] or ore >= geode_cost[0] + (geode_cost[0] - ore_rs) * (mn-2)
            enough_obs = obs_rs >= geode_cost[1] or obs >= geode_cost[1] + (geode_cost[1] - obs_rs) * (mn-2)
            if enough_ore and enough_obs:
                return mn*(mn-1) // 2

        if (res := memo.get(tpl)) is not None:
            return res

        res = 0
        # build one geode robot
        if ore >= geode_cost[0] and obs >= geode_cost[1]:
            res = max(res, mn-1+get((mn-1, ore-geode_cost[0]+ore_rs, clay+clay_rs, obs-geode_cost[1]+obs_rs, ore_rs, clay_rs, obs_rs)))
        # build one obsidian robot
        if ore >= obs_cost[0] and clay >= obs_cost[1] and obs_rs < max_obs_robots:
            res = max(res, get((mn-1, ore-obs_cost[0]+ore_rs, clay-obs_cost[1]+clay_rs, obs+obs_rs, ore_rs, clay_rs, obs_rs+1)))
        # build one clay robot
        if ore >= clay_cost and clay_rs < max_clay_robots:
            res = max(res, get((mn-1, ore-clay_cost+ore_rs, clay+clay_rs, obs+obs_rs, ore_rs, clay_rs+1, obs_rs)))
        # build one ore robot
        if ore >= ore_cost and ore_rs < max_ore_robots:
            res = max(res, get((mn-1, ore-ore_cost+ore_rs, clay+clay_rs, obs+obs_rs, ore_rs+1, clay_rs, obs_rs)))

        # don't waste resources
        res = max(res, get((mn-1, ore+ore_rs, clay+clay_rs, obs+obs_rs, ore_rs, clay_rs, obs_rs)))

        memo[tpl] = res
        return res

    return get((minutes, 0, 0, 0, 1, 0, 0))

def p1(data):
    answer = 0
    for line in data:
        bpid, reqs = line.split(": ")
        bpid = int(bpid.split()[-1])
        ore_cost, clay_cost, obs_cost, geode_cost = reqs.split(". ")
        ore_cost = int(ore_cost.split()[-2])
        clay_cost = int(clay_cost.split()[-2])
        obs_cost = tuple(int(w) for w in obs_cost.split() if w.isdigit())
        geode_cost = tuple(int(w) for w in geode_cost.split() if w.isdigit())

        res = simulate(24, ore_cost, clay_cost, obs_cost, geode_cost)
        print(bpid, res)
        answer += bpid * res
    return answer

def p2(data):
    minutes = int(argv[1])
    print(minutes)
    answer = 1
    for line in data[:3]:
        bpid, reqs = line.split(": ")
        bpid = int(bpid.split()[-1])
        ore_cost, clay_cost, obs_cost, geode_cost = reqs.split(". ")
        ore_cost = int(ore_cost.split()[-2])
        clay_cost = int(clay_cost.split()[-2])
        obs_cost = tuple(int(w) for w in obs_cost.split() if w.isdigit())
        geode_cost = tuple(int(w) for w in geode_cost.split() if w.isdigit())

        res = simulate(minutes, ore_cost, clay_cost, obs_cost, geode_cost)
        print(bpid, res)
        answer *= res
    return answer

if __name__ == '__main__':
    # print(f"part1 = {p1(data)}")
    print(f"part2 = {p2(data)}")
