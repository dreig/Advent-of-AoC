require "bundler/inline"
gemfile do
  source "https://rubygems.org"
  gem "debug"
  gem "bitset"
end

filename = ARGV[0]
Command = Struct.new(:stat, :x, :y, :z)
@commands = []

File.foreach(filename).map do |line|
  break if line.strip.empty?
  m = line.match(/(?<turn>on|off)\s+(?<x>.*),(?<y>.*),(?<z>.*)/)
  coords = m.values_at(:x,:y,:z).map { |cc| cc.split(/(=|\.\.)/).values_at(2,4).map(&:to_i) }
  @commands.push Command.new(m[:turn] == "on", *coords)
end

# @commands.each do |com|
#   puts "#{com.stat ? "on" : "off"} x=#{com.x.join("..")},y=#{com.y.join("..")},z=#{com.z.join("..")}"
# end
def solve_p1
  core = Array.new(101) { Array.new(101) { Array.new(101, false) } }
  @commands.each do |com|
    next if com.x.map(&:abs).max > 50 ||
            com.y.map(&:abs).max > 50 ||
            com.z.map(&:abs).max > 50

    for x in Range.new(*com.x.map { _1 + 50})
      for y in Range.new(*com.y.map { _1 + 50})
        for z in Range.new(*com.z.map { _1 + 50})
          core[x][y][z] = com.stat
        end
      end
    end
  end
  core.sum { |x| x.sum { |y| y.sum { _1 ? 1 : 0 }}}
end

puts "P1: #{solve_p1}"

# remap coordinates to their ordinal values, and then bruteforce the solution
# (that is, if we have N commands to execute, we can remap all x,y and z coordinates into the interval [0,2*N])
# runs ~1min on my input and my machine
def solve_p2
  coms = @commands.map do |cc|
    x,y,z = [cc.x,cc.y,cc.z].map { [_1,_2+1]}
    Command.new(cc.stat, x,y,z)
  end

  xs = coms.map(&:x).flatten.sort.uniq
  ys = coms.map(&:y).flatten.sort.uniq
  zs = coms.map(&:z).flatten.sort.uniq
  coms.map! do |cc|
    x = cc.x.map { |target| xs.bsearch_index { |el| target <=> el } }
    y = cc.y.map { |target| ys.bsearch_index { |el| target <=> el } }
    z = cc.z.map { |target| zs.bsearch_index { |el| target <=> el } }
    Command.new(cc.stat, x,y,z)
  end

  n = coms.size * 2
  core = Array.new(n) { Array.new(n) { Bitset.new(n) }}
  coms.each_with_index do |com,i|
    for x in Range.new(*com.x, true)
      for y in Range.new(*com.y, true)
        for z in Range.new(*com.z, true)
          core[x][y][z] = com.stat
        end
      end
    end
  end

  ans = 0
  core.each_with_index do |yz, i|
    yz.each_with_index do |z, j|
      z.each_with_index do |cell, k|
        if cell
          ans += (xs[i+1]-xs[i])*(ys[j+1]-ys[j])*(zs[k+1]-zs[k])
        end
      end
    end
  end
  ans
end

puts "P2: #{solve_p2}"

