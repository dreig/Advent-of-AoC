require 'debug'
filename = ARGV[0]

floor = File.read(filename).split.map { _1.strip.scan(/\d/).map(&:to_i) }.reject(&:empty?)

floor.each { _1.unshift(9).push(9) }
width  = floor[0].size
floor.unshift(Array.new(width, 9)).push(Array.new(width, 9))
height = floor.size

p1_ans = 0

for i in 1...height-1
  for j in 1...width-1
    [[-1,0],[1,0],[0,-1],[0,1]].map { floor[i+_1][j+_2] }.compact.min.then do |mn|
      if floor[i][j] < mn
        p1_ans += floor[i][j] + 1
      end
    end
  end
end

puts p1_ans

vis = Array.new(height) { Array.new(width, nil) }

sizes = []
for i in 1...height-1
  for j in 1...width-1
    next unless (vis[i][j].nil? && floor[i][j] < 9)
    sz = 0
    qu = [[i,j]]
    while !qu.empty?
      x,y = qu.shift
      if vis[x][y].nil?
        vis[x][y] = true
        sz += 1
        [[-1,0],[1,0],[0,-1],[0,1]].each do
          ni = x+_1
          nj = y+_2
          if vis[ni][nj].nil? && floor[ni][nj] < 9
            qu.push([ni, nj])
          end
        end
      end
    end
    sizes.push(sz)
  end
end

sizes.sort!.reverse!
p sizes.take(3).reduce(1, :*)
