require "debug"
filename = ARGV[0]

INF = 10**9
bd = File.readlines(filename).map(&:strip).map { _1.split(//).map(&:to_i) }

wd = bd.first.size
ht = bd.size
width = wd*5
height = ht*5

board = Array.new(height) { Array.new(width, 0) }
for n in 0..4
  for m in 0..4
    offY = n*ht
    offX = m*wd
    add = n + m
    for i in 0...ht
      for j in 0...wd
        c = bd[i][j] + add
        c -= 9 if c >= 10
        board[offY+i][offX+j] = c
      end
    end
  end
end

cost = Array.new(height) { Array.new(width, INF) }
vis = Array.new(height) { Array.new(width, nil) }
cost[0][0] = 0

cind = 0
qu = [[[0,0]]]
while cind < qu.size
  (cind += 1 and next) if (qu[cind] ||= []).empty?
  cc = cind
  i,j = qu[cc].pop
  next if vis[i][j]
  cost[i][j] = cc
  vis[i][j] = true
  break if i == height-1 && j == width-1
  [[-1,0],[1,0],[0,-1],[0,1]].map {[i+_1, j+_2]}.each do |ni, nj|
    next if ni <0 || nj <0 || ni >= height || nj >= width || vis[ni][nj]
    new_cc = cc + board[ni][nj]
    (qu[new_cc] ||= []).push([ni,nj])
  end
end

p cost[-1][-1]
