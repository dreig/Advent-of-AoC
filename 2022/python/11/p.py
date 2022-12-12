#!/usr/bin/env python
import re
from sys import stdin
import operator
from math import lcm

lines = [line.strip() for line in stdin.readlines()]

class MonkeyRegistry:
    def __init__(self, monkeys = None):
        self.monkeys = [] if monkeys is None else [m for m in monkeys]

    def add_monkey(self, monkey):
        self.monkeys.append(monkey)

    def get_monkey(self, id):
        return self.monkeys[id]

class Monkey:
    MOD = lcm(2,3,5,7,11,13,17,19,23)

    def __init__(self, registry, operation, test, idTrue, idFalse, items=None):
        self.registry = registry
        self.items = [] if items is None else [it for it in items]
        self.operation = operation
        self.test = test
        self.idTrue = idTrue
        self.idFalse = idFalse

        self._item_counter = 0
        self.registry.add_monkey(self)

    @property
    def item_counter(self):
        return self._item_counter

    def add_item(self, item):
        self.items.append(item)

    def process_items(self, worry_reduction=True):
        for item in self.items:
            item = self.operation(item)
            if worry_reduction:
                item = item // 3
            else:
                item = item % self.MOD
            targetId = self.idTrue if self.test(item) else self.idFalse

            self.registry.get_monkey(targetId).add_item(item)
            self._item_counter += 1
        self.items = []

OPERATORS = {
    "+": operator.add,
    "*": operator.mul,
}

def build_monkey(data, registry):
    m_id, *body = data
    items, operation, test, idTrue, idFalse = [line.split(":")[1].strip() for line in body]

    idTrue = int(idTrue.split()[-1])
    idFalse = int(idFalse.split()[-1])

    divisor = int(test.split()[-1])
    test = lambda n: n % divisor == 0

    lhs, op, rhs = operation.split("=")[1].strip().split()
    op = OPERATORS[op]
    def _operation(n):
        nonlocal lhs, rhs, op
        x = n if lhs == "old" else int(lhs)
        y = n if rhs == "old" else int(rhs)
        return op(x, y)
    operation = _operation

    items = [int(it) for it in items.split(",")]
    Monkey(registry, operation, test, idTrue, idFalse, items)

def split_into_monkeys(lines):
    res = []
    start = 0
    for i, line in enumerate(lines + [""]):
        if not line:
            res.append(lines[start:i])
            start = i+1

    return res

def solve(rounds=20, worry_reduction=True):
    registry = MonkeyRegistry()
    for data in split_into_monkeys(lines):
        build_monkey(data, registry)

    for r in range(1, rounds+1):
        for m in registry.monkeys:
            m.process_items(worry_reduction)

    cnt = [m.item_counter for m in registry.monkeys]

    x,y = sorted(cnt, reverse=True)[:2]
    return x*y

if __name__ == '__main__':
    print(f"part1: {solve()}")
    print(f"part2: {solve(rounds=10000, worry_reduction=False)}")
