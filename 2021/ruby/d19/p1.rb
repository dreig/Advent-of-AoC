require "debug"
filename = ARGV[0]

class SN
  PERMS = [0,1,2].permutation.to_a.freeze
  REV_PERMS = PERMS.map {|perm| perm.zip([0,1,2]).sort.map(&:last) }.freeze


  # store the beacons in 6 ways, for each permutation of [x,y,z] coordinates
  attr_reader :perms
  # for each permutation of [x,y,z] store the 6 extremal points
  # (min x, max x, min y, max y, min z, max z)
  # we use these to compute the relative vectors and compare them to the relative vectors of beacons of other scanners.
  attr_reader :extremes

  def initialize(beacons)
    @perms = PERMS.map do |perm|
      perm.zip(beacons.transpose).sort.map(&:last).transpose.sort
    end
    @extremes = @perms.map do |perm|
      [0,1,2].map do |ind|
        perm.minmax_by { _1[ind] }
      end.flatten(1).uniq
    end
  end
end

def read_and_parse(filename)
  result = []
  cur_scanner = nil

  File.foreach(filename) do |line|
    line.strip!
    if line.empty?
      break if cur_scanner.nil?
      result.push(SN.new(cur_scanner))
      cur_scanner = nil
      next
    end

    if (cc = line.match(/scanner\s+(\d+)/))
      cur_scanner = []
    else
      cur_scanner.push(line.split(',').map(&:to_i))
    end
  end
  if !cur_scanner.nil?
    result.push(SN.new(cur_scanner))
    cur_scanner = nil
  end
  return result
end

@ss = read_and_parse(filename)
# mark scanners whose beacon data has been merged
@reached = @ss.map { false }
# offset from the first scanner: 'scanner 0'
@scanner_offset = @ss.map { [] }

def have_intersection(s, t)
  s.perms.each do |perm|
    perm.each do |a1,b1,c1|
      norm1 = perm.map { |x1,y1,z1| [x1-a1,y1-b1,z1-c1] }
      tperm = t.perms[0]
      tperm.each do |a2,b2,c2|
        norm2 = tperm.map { |x2,y2,z2| [x2-a2,y2-b2,z2-c2] }
        [1,-1].repeated_permutation(3).each do |dir1,dir2,dir3|
          n2 = norm2.map { |x,y,z| [x*dir1, y*dir2, z*dir3] }
          if (norm1.intersection(n2)).size >= 12
            return true
          end
        end
      end
    end
  end
  false
end

@queue = []
# Find all scanners that have overlapping data with the given scanner
# Update the coordinates of the target scanner to coordinates relative to the 'scanner 0'
def update_overlapping(src)
  @ss[src].perms.each.with_index do |perm, pi|
    @ss[src].extremes[pi].each do |a1, b1, c1|
      norm1 = perm.map { |x1,y1,z1| [x1-a1,y1-b1,z1-c1] }
      [-1,1].repeated_permutation(3).each do |d1,d2,d3|
        n1 = norm1.map {|x,y,z| [x*d1, y*d2, z*d3] }
        @ss.each.with_index do |target, ti|
          next if @reached[ti]

          t = target.perms[0]
          t.each do |a2,b2,c2|

            n2 = t.map { |x2,y2,z2| [x2-a2,y2-b2,z2-c2] }
            if (n1.intersection(n2)).size >= 12
              # scanner src and 't' have overlapping beacons
              @reached[ti] = true
              @queue.push(ti)
              # update_coordinates of the target beacons
              upd_perm = t.map { |x,y,z| [(x-a2)*d1 + a1, (y-b2)*d2 + b1, (z-c2)*d3 +c1] }
              offset_perm = [a2*d1-a1, b2*d2-b1, c2*d3-c1]
              # reverse the permutation of the target beacons
              upd = SN::REV_PERMS[pi].zip(upd_perm.transpose).sort.map(&:last).transpose
              offset = SN::REV_PERMS[pi].zip(offset_perm).sort.map(&:last)
              @ss[ti] = SN.new(upd)
              @scanner_offset[ti] = offset
              break
            end
          end
        end
      end
    end
  end
end

# starting from the original scanner, find all overlapping scanners, and update their coordinates, then re-launch the procedure from the newly reached scanners.
# We assume that we can reach every scanner by moving from a scanner to its neighbors. (that is, there is no scanner, that requires the union of data from multiple scanners to be reached.)
def solve
  @reached[0] = true
  @queue.push(0)
  @scanner_offset[0] = [0,0,0]
  while !@queue.empty?
    p @queue
    src = @queue.shift
    update_overlapping(src)
  end
end

# the solution runs ~1min on my input
solve()

beacons = @ss.map { _1.perms[0] }.flatten(1).uniq
puts "P1: #{beacons.size}"
p2_ans = @scanner_offset.map do |x1,y1,z1|
            @scanner_offset.map do |x2,y2,z2|
              (x1-x2).abs + (y1-y2).abs + (z1-z2).abs
            end.max
          end.max
puts "P2: #{p2_ans}"
