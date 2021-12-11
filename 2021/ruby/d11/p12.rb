require "debug"
filename = ARGV[0]

board = File.read(filename).strip.split.map{ _1.split(//).map(&:to_i) }
@dirs = (-1..1).map { (-1..1).zip([_1].cycle) }.flatten(1)
@dirs.delete([0,0])

def iteration(bd)
  flash_count = 0
  flash = Array.new(10) { Array.new(10, nil) }
  qu = []
  for i in 0..9
    for j in 0..9
      bd[i][j] += 1
      if bd[i][j] > 9
        qu.push([i,j])
      end
    end
  end
  while !qu.empty?
    i,j = qu.shift
    next if flash[i][j]
    bd[i][j] = 0
    flash[i][j] = true
    flash_count += 1
    @dirs.map { [i+_1, j+_2] }.each do |ni, nj|
      next if ni < 0 || ni > 9 || nj < 0 || nj > 9 || flash[ni][nj]
      bd[ni][nj] += 1
      qu.push([ni, nj]) if bd[ni][nj] > 9
    end
  end
  flash_count
end

p1_ans = 0
p2_ans = 0
total = 0
(1..).each do |n|
  delta = iteration(board)
  total += delta
  p1_ans = total if n == 100
  if delta == 100
    p2_ans = n
    break
  end
end

puts "P1: #{p1_ans}"
puts "P2: #{p2_ans}"
