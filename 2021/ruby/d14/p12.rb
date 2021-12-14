require "debug"
filename = ARGV[0]

BASE = 30
@rule = {}
@mapping = {}
def registerKey(key)
  @mapping.fetch(key) do
    @mapping[key] = @mapping.size
  end
end

def ruleHash(arr)
  arr.reduce(0) { _1 * BASE + _2 }
end

contents = File.readlines(filename).map(&:strip).reject(&:empty?)
polymer = contents.shift.chars.map! { registerKey(_1) }

rules = contents.map do |line|
  input, output = line.split("->").map(&:strip)
  input = input.chars.map { registerKey(_1) }
  output = registerKey(output[0])
  key = ruleHash(input)
  values = [[input.first, output], [output, input.last]].map { ruleHash(_1) }
  @rule[key] = values
end

def updatePairs(prs)
  new_pairs = Hash.new(0)
  prs.each do |pair, cnt|
    @rule[pair].each { new_pairs[_1] += cnt }
  end
  new_pairs
end


def solve(polymer, iterations)
  pairs = polymer.each_cons(2).map { ruleHash(_1) }.tally
  final_pairs = (1..iterations).reduce(pairs) { updatePairs(_1) }

  final_tally = Hash.new(0)
  final_pairs.each do |pair, cnt|
    pair.divmod(BASE).each { final_tally[_1] += cnt }
  end

  # each base (except for the first and last) are counted twice. we need to adjust the final tally accordingly
  final_tally[polymer.first] += 1
  final_tally[polymer.last] += 1
  final_tally.transform_values! { _1 / 2 }

  final_tally.values.sort.then { _1.last - _1.first }
end

p1_answer = solve(polymer, 10)
puts "P1: #{p1_answer}"

p2_answer = solve(polymer, 40)
puts "P2: #{p2_answer}"
