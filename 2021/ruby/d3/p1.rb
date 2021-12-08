filename = ARGV[0]

bits = [[], []]

File.foreach(filename) do |line|
  line.strip!
  break if line == ""

  line.each_char.map(&:to_i).each.with_index do |ch, i|
    bits[ch][i] ||= 0
    bits[ch][i] += 1
  end
end

@len = bits[0].size

gamma = Array.new(@len)
epsilon = Array.new(@len)

@len.times do |i|
  if bits[0][i] > bits[1][i]
    gamma[i] = 0
    epsilon[i] = 1
  else
    gamma[i] = 1
    epsilon[i] = 0
  end
end

puts gamma.join("").to_i(2) * epsilon.join("").to_i(2)
