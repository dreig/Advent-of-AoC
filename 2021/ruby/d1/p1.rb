filename = ARGV[0]

ans = 0
window = []
interval = 3 # for PartI change to 1

File.foreach(filename) do |line|
  line.strip!
  break if line == ""

  cur = line.to_i
  if window.size >= interval
    ans += 1 if cur > window.first
    window.shift
  end
  window.push(cur)
end

puts ans
