require "debug"
filename = ARGV[0]

def cost(n)= n*(n+1)/2

numbers = File.read(filename).strip.split(',').map(&:to_i).sort
p1_ans = (numbers.size)**3
Range.new(*numbers.minmax).each do |n|
  p1_ans = [p1_ans, numbers.map { (_1 - n).abs }.sum].min
end
puts p1_ans

p2_ans = (numbers.size)**3
Range.new(*numbers.minmax).each do |n|
  p2_ans = [p2_ans, numbers.map { cost((_1 - n).abs) }.sum].min
end
puts p2_ans
