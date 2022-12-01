#!/usr/bin/env python
from sys import stdin

data = [line.strip() for line in stdin.readlines()]

OP = "["
CL = "]"

def parse(line):
   res = []
   number, in_progress = 0, False
   for c in line:
      if c.isdigit():
         number = number * 10 + int(c)
         in_progress = True
      else:
         if in_progress:
            res.append(number)
            number = 0
            in_progress = 0
         if c != ",":
            res.append(c)

   return res

def explode(line):
   op = 0
   left = -1
   for i,c in enumerate(line):
      if c == OP: op += 1
      elif c == CL: op -=1

      if op == 5:
         left = i
         break

   if left == -1:
      return line, False

   right = left + line[left:].index(CL)

   a,b = line[left+1:right]
   for i in range(left-1, -1, -1):
      if line[i] not in (OP, CL):
         line[i] += a
         break
   for i in range(right, len(line)):
      if line[i] not in (OP, CL):
         line[i] += b
         break
   return line[:left] + [0] + line[right+1:], True

def split(line):
   for i, c in enumerate(line):
      if c not in (OP, CL) and c >= 10:
         line[i:i+1] = [OP, c // 2, (c+1) // 2, CL]
         return line, True

   return line, False

def simplify(line):
   while True:
      line, ok = explode(line)
      if ok:
         continue
      line, ok = split(line)
      if ok:
         continue
      break
   return line

def add(a,b):
   return simplify([OP] + a + b + [CL])

def magnitude(line):
   """returns magnitude of consumed and start of the leftover"""
   if not line:
      return 0, []
   if line[0] == OP:
      left, line = magnitude(line[1:]) # skip OP. next elements starts with line
      right, line = magnitude(line)
      return 3*left + 2*right, line[1:] # skip CL.

   if line[0] == CL:
      return 0, line[1:]

   return line[0], line[1:]

def p1(data):
   res, *data = map(parse, data)
   for line in data:
      res = add(res, line)
   answer, _ =  magnitude(res)
   return answer

def p2(data):
   lines = [parse(line) for line in data]
   answer = max(magnitude(add(a,b))[0] for (i,a) in enumerate(lines)
         for (j,b) in enumerate(lines) if i != j)
   return answer

if __name__ == '__main__':
   print(p1(data))
   print(p2(data))
