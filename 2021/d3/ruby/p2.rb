filename = ARGV[0]

numbers = []
@len = nil

File.foreach(filename) do |line|
  line.strip!
  break if line == ""
  @len = line.size if @len.nil?

  numbers.push(line.reverse.to_i(2))
end

def next_prefix_candidates(pref, pos, numbers)
  prefix_hash = Hash.new(0)
  pref_mask = (1 << (pos-1)) - 1 # to filter numbers
  mask = (1 << pos) - 1          # to compute the next prefix
  numbers.each do |num|
    if num & pref_mask == pref
      cand = num & mask
      prefix_hash[cand] += 1
    end
  end

  prefix_hash
end

oxygen = (1..@len).inject(0) do |pref, pos|
  next_prefix_hash = next_prefix_candidates(pref, pos, numbers)

  next_prefix_hash.max_by {|k, v| [v,k]}.first
end

scrubber = (1..@len).inject(0) do |pref, pos|
  next_prefix_hash = next_prefix_candidates(pref, pos, numbers)

  next_prefix_hash.min_by {|k, v| [v, k]}.first
end


print oxygen, "\t", oxygen.to_s(2).rjust(@len, '0'), "\n"
print scrubber, "\t", scrubber.to_s(2).rjust(@len, '0'), "\n"

puts oxygen * scrubber
