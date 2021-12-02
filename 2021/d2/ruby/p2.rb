filename = ARGV[0]

posx, posy = 0, 0
aim  = 0

File.foreach(filename) do |line|
  line.strip!
  break if line == ""

  dir, move = line.split
  move = move.to_i
  case dir
  when "forward"
    posx += move
    posy += aim * move
  when "down" then aim += move
  when "up"   then aim -= move
  end
end

puts "posx=#{posx}, posy=#{posy}, aim=#{aim}"

puts posx * posy
