require "debug"
filename = ARGV[0]

board = File.readlines(filename).map(&:strip).map { _1.split(//).map(&:to_i) }

height = board.size
width = board.first.size
INF = 10**9

cost = Array.new(height) { Array.new(width, INF) }
vis = Array.new(height) { Array.new(width, nil) }
cost[0][0] = 0

qu = [[0,0,0]]

while !qu.empty?
  nbr, index =  qu.each.with_index.min_by { _1 }
  qu.delete_at(index)
  cc, i, j = nbr
  next if vis[i][j]
  cost[i][j] = cc
  vis[i][j] = true
  break if i == height-1 && j == width-1
  [[-1,0],[1,0],[0,-1],[0,1]].map { [i+_1, j+_2] }.each do |ni, nj|
    next if ni <0 || nj <0 || ni >= height || nj >= width || vis[ni][nj]
    qu.push([cc + board[ni][nj], ni, nj])
  end
end

p cost[-1][-1]
