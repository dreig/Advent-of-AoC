import sys

data = [int(line.strip()) for line in sys.stdin.readlines()]
def count_increasing(data):
    return sum(nxt > prev for (nxt, prev) in zip(data[1:], data))

def three_window(data):
    return [a+b+c for (a,b,c) in zip(data, data[1:], data[2:])]

if __name__ == '__main__':
    print(count_increasing(data))
    print(count_increasing(three_window(data)))
