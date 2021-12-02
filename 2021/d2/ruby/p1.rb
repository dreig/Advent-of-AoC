filename = ARGV[0]

posx, posy = 0, 0

File.foreach(filename) do |line|
  line.strip!
  break if line == ""

  dir, move = line.split
  move = move.to_i
  case dir
  when "forward" then posx += move
  when "down"    then posy += move
  when "up"      then posy -= move
  end
end

puts "posx=#{posx}, posy=#{posy}"

puts posx * posy
