require "debug"
require "set"
filename = ARGV[0]

points, folds = File.readlines(filename).map(&:strip)
                    .chunk(&:empty?)
                    .reject { _1.first }
                    .map(&:last)

Point = Struct.new(:x, :y)

def foldX(val)
  lambda do |pt|
    x = pt.x > val ? 2*val - pt.x : pt.x
    Point.new(x, pt.y)
  end
end

def foldY(val)
  lambda do |pt|
    y = pt.y > val ? 2*val - pt.y : pt.y
    Point.new(pt.x, y)
  end
end

points.map! {|line| Point.new(*line.split(',').map(&:to_i)) }

folds.map! do |line|
  xy, value = line.match(/([xy])=(\d+)/).captures
  xy == "x" ? foldX(value.to_i) : foldY(value.to_i)
end

p1_answer = points.map {|pt| folds[0].(pt) }.uniq.size

puts "P1: #{p1_answer}"

p2_points = points.map { |pt| folds.reduce(pt) { |res, f| f.(res) }}.uniq

x_max = p2_points.max_by(&:x).x + 1
y_max = p2_points.max_by(&:y).y + 1
board = Array.new(y_max) { '.' * x_max }
p2_points.each { |pt| board[pt.y][pt.x] = '#' }
puts "P2:"
puts board
