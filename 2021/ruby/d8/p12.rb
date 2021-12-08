require "debug"
require "set"
filename = ARGV[0]

p1_ans = 0
p2_ans = 0

File.foreach(filename) do |line|
  line.strip!
  break if line.empty?

  mapping = Array.new(10, "")

  digits, display = line.split("|").map { _1.strip.split(' ').reject(&:empty?).map { |word| Set.new(word.chars) } }

  digits = digits.group_by { _1.size }
  {2=>1, 3 => 7, 4 => 4, 7 => 8 }.each { mapping[_2] = digits[_1].first }

  mapping[3] = digits[5].select { _1.superset? mapping[1] }.first
  digits[5].delete(mapping[3])

  mapping[9] = digits[6].select { _1.superset? mapping[4] }.first
  digits[6].delete(mapping[9])

  mapping[0] = digits[6].select { _1.superset? mapping[1] }.first
  digits[6].delete(mapping[0])

  mapping[6] = digits[6].first

  (mapping[8] - mapping[9]).then do |letter_e|
    mapping[2] = digits[5].select { _1.superset? letter_e }.first
    digits[5].delete(mapping[2])
  end

  mapping[5] = digits[5].first

  output = mapping.zip(0..9).to_h.then do |digit_hash|
    display.map { digit_hash[_1] }
  end

  p1_ans += output.select { [1,4,7,8].include? _1 }.count
  output = output.reduce(0) { _1*10 + _2}

  p2_ans += output
end

p p1_ans
p p2_ans
