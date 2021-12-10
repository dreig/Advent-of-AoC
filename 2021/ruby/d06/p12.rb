require "debug"
filename = ARGV[0]

@fish = Array.new(9, 0)
File.read(filename).strip.split(',').map(&:to_i).tally.each { |k,v| @fish[k] += v }

days = 256
(1..days).each do |n|
  next_gen = Array.new(9, 0)
  next_gen[6] = @fish[0]
  next_gen[8] = @fish[0]
  @fish.drop(1).each.with_index(0) { |v, i| next_gen[i] += v }
  @fish = next_gen
end

p @fish.sum
