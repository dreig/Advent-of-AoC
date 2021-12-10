require 'debug'

filename = ARGV[0]

class Board
  def initialize(rows)
    @mark = Array.new(5) { Array.new(5, false) }
    # assume rows is 5x5 array
    @data = rows
    @done = false
  end

  def mark(number)
    for i in 0..4 do
      for j in 0..4 do
        if @data[i][j] == number
          # this assumes that numbers on a board are distinct, and we can stop at the first match
          # must reconsider the approach otherwise
          @mark[i][j] = true
          return i,j
        end
      end
    end
    return -1,-1
  end

  def bingo?(x, y)
    return false if x == -1 || y == -1
    @mark.map {|r| r[y]}.all? ||
    @mark.transpose.map {|r| r[x]}.all?
  end

  def score(x, y)
    return -1 if x == -1 || y == -1

    total = 0
    for i in 0..4 do
      for j in 0..4 do
        if !@mark[i][j]
          total += @data[i][j]
        end
      end
    end
    total * @data[x][y]
  end

  def done!; @done = true; end
  def done?; @done; end
end

def read_board(lines, ind)
  ind += 1 while ind < lines.size && lines[ind] == ""
  rows = []
  while ind < lines.size && lines[ind] != ""
    row = lines[ind].split.map(&:to_i)
    rows.push(row)
    ind += 1
  end
  board = Board.new(rows) unless rows.empty?
  return ind, board
end

@lines = File.readlines(filename).map(&:strip)
@numbers = @lines.shift.split(',').map(&:to_i)

@boards = []
ind = 0
while ind < @lines.size
  ind, new_board = read_board(@lines, ind)
  @boards.push(new_board) unless new_board.nil?
end

def part1
  @numbers.each do |num|
    @boards.each do |board|
      i,j = board.mark(num)
      if board.bingo?(i,j)
        return board.score(i,j)
      end
    end
  end
end

def part2
  last_score = 0
  @numbers.each do |num|
    @boards.each do |board|
      i, j = board.mark(num)
      if !board.done? && board.bingo?(i,j)
        last_score = board.score(i, j)
        board.done!
      end
    end
  end
  return last_score
end

# puts part1
puts part2

