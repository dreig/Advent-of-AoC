require "debug"
filename = ARGV[0]
pos = File.readlines(filename).map(&:strip).reject(&:empty?)
          .map { _1.scan(/\d+/).last.to_i }

score = [0,0]
cur = 0 # 0 or 1
cnt = 0
(1..100).cycle.each_slice(3) do |d1,d2,d3|
  cnt += 3
  s = d1+d2+d3
  pos[cur] = (pos[cur] + s - 1) % 10 + 1
  score[cur] += pos[cur]
  if (score[cur] >= 1000)
    puts cnt * score[1-cur]
    break
  end
  cur = 1-cur
end

