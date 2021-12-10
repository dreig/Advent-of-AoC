require "debug"
filename = ARGV[0]

score_card_p1 = ")]}>".chars.zip([3,57,1197,25137]).to_h
score_card_p2 = ")]}>".chars.zip(1..4).to_h
match_open_par = "()[]{}<>".chars.each_slice(2).to_a.to_h
match_close_par = "()[]{}<>".chars.each_slice(2).to_a.map(&:reverse).to_h

p1_score = 0
corrupt_pars = []

p2_scores = []

File.foreach(filename) do |line|
  line.strip!
  break if line.empty?
  st = []
  corrupted = false
  line.chars.each do |c|
    if "([{<".include? c
      st.push(c)
    else
      mp = match_close_par.fetch(c)
      if st.last == mp
        st.pop
      else
        corrupt_pars.push(c)
        p1_score += score_card_p1.fetch(c)
        corrupted = true
        break
      end
    end
  end

  next if corrupted
  score = 0
  st.reverse.map { match_open_par[_1] }.each do |c|
    score = score * 5 + score_card_p2.fetch(c)
  end
  p2_scores.push(score)
end

p p1_score
p p2_scores.sort[p2_scores.size/2]
