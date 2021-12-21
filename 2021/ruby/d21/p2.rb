require "debug"
filename = ARGV[0]
start_pos = File.readlines(filename).map(&:strip).reject(&:empty?)
          .map { _1.scan(/\d+/).last.to_i }


scoreF= [0,0,0,1,3,6,7,6,3,1]

# number of wins in turns
p1_turns = Array.new(15, 0)
p2_turns = Array.new(15, 0)

dp1 = Array.new(11) { Array.new(22, 0) }
dp2 = Array.new(11) { Array.new(22, 0) }

dp1[start_pos[0]][0] = 1
dp2[start_pos[1]][0] = 1

14.times do |turn|
  tmp = Array.new(11) { Array.new(22, 0) }
  for pos in 1..10
    for score in 0..20
      next if dp1[pos][score] == 0
      for add in 3..9
        cnt = scoreF[add]
        new_pos = (pos + add - 1) % 10 + 1
        new_score = [score + new_pos, 21].min
        tmp[new_pos][new_score] += dp1[pos][score] * cnt
      end
    end
  end
  for pos in 1..10
    p1_turns[turn+1] += tmp[pos][21]
  end
  dp1 = tmp
end

14.times do |turn|
  tmp = Array.new(11) { Array.new(22, 0) }
  for pos in 1..10
    for score in 0..20
      next if dp2[pos][score] == 0
      for add in 3..9
        cnt = scoreF[add]
        new_pos = (pos + add - 1) % 10 + 1
        new_score = [score + new_pos, 21].min
        tmp[new_pos][new_score] += dp2[pos][score] * cnt
      end
    end
  end
  for pos in 1..10
    p2_turns[turn+1] += tmp[pos][21]
  end
  dp2 = tmp
end

wins1 = 0
for turn in 1..14
  next if p1_turns[turn] == 0
  not_wins = p2_turns.take(turn).reverse.reject(&:zero?).zip((0..15).map {27**_1}).map {|u,v| u*v}

  wins1 += p1_turns[turn] * (27**(turn-1) - not_wins.sum)

end

wins2 = 0
for turn in 1..14
  next if p2_turns[turn] == 0
  not_wins = p1_turns.take(turn+1).reverse.reject(&:zero?).zip((0..15).map {27**_1}).map {|u,v| u*v}

  wins2 += p2_turns[turn] * (27**turn - not_wins.sum)
end

puts "P2: #{[wins1,wins2].max}"
