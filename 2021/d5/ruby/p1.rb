require "debug"

filename = ARGV[0]
Point = Struct.new(:x, :y)
Segment = Struct.new(:a, :b) do
  def horizontal?() = a.y == b.y
  def vertical?()   = a.x == b.x
  def diag1?() = a.x-a.y == b.x-b.y
  def diag2?() = a.x+a.y == b.x+b.y
end

@segments = []

File.foreach(filename) do |line|
  line.strip!
  break if line == ""

  line.split("->").map(&:strip).map do |endpoint|
    Point.new *endpoint.split(",").map(&:to_i)
  end.then do |ends|
    segment = Segment.new(*ends)
    @segments.push segment
  end
end

xmax = 2 + @segments.max_by {|s| [s.a.x, s.b.x].max }
                    .then {|s| [s.a.x, s.b.x].max }

ymax = 2 + @segments.max_by {|s| [s.a.y, s.b.y].max }
                   .then {|s| [s.a.y, s.b.y].max }


@board = Array.new(ymax) {
  Array.new(xmax) {
    # x, y, d1, d2
    [ 0, 0, 0,  0]
  }
}

@segments.each do |seg|
  if seg.horizontal?
    y = seg.a.y
    x1, x2 = seg.a.x, seg.b.x
    x1, x2 = x2, x1 if x1 > x2
    @board[y][x1][0] += 1
    @board[y][x2+1][0] -= 1
  elsif seg.vertical?
    x = seg.a.x
    y1, y2 = seg.a.y, seg.b.y
    y1, y2 = y2, y1 if y1 > y2
    @board[y1][x][1] += 1
    @board[y2+1][x][1] -= 1
  elsif seg.diag1?
    a, b = seg.a, seg.b
    a, b = b, a if a.x > b.x
    @board[a.y][a.x][2] += 1
    @board[b.y+1][b.x+1][2] -= 1
  elsif seg.diag2?
    a, b = seg.a, seg.b
    a, b = b, a if a.y > b.y
    @board[a.y][a.x][3] += 1
    @board[b.y+1][b.x-1][3] -= 1 if b.x > 0
  end
end


p1_total, p2_total = 0, 0
for y in 0...(ymax-1)
  for x in 0...(xmax-1)
    if @board[y][x].take(2).sum > 1
      p1_total += 1
    end
    if @board[y][x].sum > 1
      p2_total += 1
    end
    @board[y][x+1][0] += @board[y][x][0]
    @board[y+1][x][1] += @board[y][x][1]
    @board[y+1][x+1][2] += @board[y][x][2]
    @board[y+1][x-1][3] += @board[y][x][3] if x > 0
  end
end

puts p1_total
puts p2_total
