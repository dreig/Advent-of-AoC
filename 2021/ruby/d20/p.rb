require "debug"
filename = ARGV[0]

HH = {'.' => 0, '#' => 1}.freeze
code, bd = File.readlines(filename).map(&:strip).chunk(&:empty?).reject { _1.first }.map(&:last)
code = code.first.chars.map { HH.fetch(_1) }
bd.map! {|row| row.chars.map { HH.fetch(_1) }}

# For my particular input code[0] = 1 and code[511] = 0,
# which means that the infinite board (beyond the given image) alternates between being lit and being dim.
# I use these hardcoded values to extend the board accordingly on each iteration.
# The algorithm might have to be adjusted if: code[0] != 1 or code[511] != 0
@iter = 0 # parity of the current operation (0 or 1)
FILL = [0,(code[0] == 1 ? 1 : 0)].freeze

# add a border of "." (or '#') around the board
def extend_board(bd)
  filling = FILL[@iter]
  bd.each { _1.unshift(filling).push(filling) }
  bd[0].size.then { |n| bd.unshift(Array.new(n, filling)).push(Array.new(n, filling)) }
end

def iterate(board, code)
  if [0,-1].map { board[_1] }.map(&:sum).any?(&:nonzero?) ||
    board.map { _1.values_at(0,-1) }.transpose.map(&:sum).any?(&:nonzero?)
    extend_board(board)
  end

  h = board.size
  w = board[0].size
  new_bd = Array.new(h) { Array.new(w, 0)}
  for i in 0...h
    for j in 0...w
      bin = [-1,0,1].product([-1,0,1]).map do |di, dj|
        if i + di < 0 || i + di >= h || j + dj < 0 || j + dj >= w
          FILL[@iter]
        else
          board[i+di][j+dj]
        end
      end.reduce(0) { _1*2 + _2 }
      new_bd[i][j] = code[bin]
    end
  end
  @iter = 1 - @iter
  return new_bd
end

bd2 = 2.times.reduce(bd) { iterate(_1, code) }
puts "P1: #{ bd2.sum { _1.sum } }"

bd50 = 50.times.reduce(bd) { iterate(_1, code) }
puts "P2: #{ bd50.sum { _1.sum } }"
