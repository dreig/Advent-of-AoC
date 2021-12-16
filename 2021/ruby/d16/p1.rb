require "stringio"
require "debug"
filename = ARGV[0]

Packet = Struct.new(:version, :type_id, :lit_value, :subpackets, keyword_init: true) do
  def initialize(...)
    super
    self.subpackets ||= []
  end

  def total_versions
    version + subpackets.sum { _1.total_versions }
  end

  def val
    return lit_value if type_id == 4

    subs = subpackets.map(&:val)
    case type_id
    when 0 then subs.reduce(:+)
    when 1 then subs.reduce(:*)
    when 2 then subs.min
    when 3 then subs.max
    when 5 then subs[0] > subs[1] ? 1 : 0
    when 6 then subs[0] < subs[1] ? 1 : 0
    when 7 then subs[0] == subs[1] ? 1 : 0
    end
  end
end

def parse(hex_encoded_str)
  hex_encoded_str.strip.chars.map { _1.to_i(16).to_s(2).rjust(4,'0') }.join
end

def read_packet(io)
  version = io.read(3).to_i(2)
  type_id = io.read(3).to_i(2)
  packet = Packet.new(version: version, type_id: type_id)
  if type_id == 4
    packet.lit_value = read_literal(io)
  else
    len_type_id = io.read(1).to_i(2)
    if len_type_id == 0
      length = io.read(15).to_i(2)

      pos = io.pos
      subpackets = []
      while io.pos < pos + length
        subpackets.push(read_packet(io))
      end
    else
      num = io.read(11).to_i(2)
      subpackets = num.times.map { read_packet(io) }
    end
    packet.subpackets = subpackets
  end
  packet
end

def read_literal(io)
  str = ""
  loop do
    frag = io.read(5)
    str += frag[1..]
    break if frag[0] == '0'
  end
  str.to_i(2)
end

=begin
puts ("p1").center(60, '-')
examples_p1 = %w[
  8A004A801A8002F478
  620080001611562C8802118E34
  C0015000016115A2E0802F182340
  A0016C880162017C3686B18A3D4780
]
examples_p1.each do |str|
  print str.ljust(30), "\t"
  p read_packet(StringIO.new(parse(str))).total_versions
end

puts ("p1").center(60, '-')
examples_p2 = %w[
  C200B40A82
  04005AC33890
  880086C3E88112
  CE00C43D881120
  D8005AC2A8F0
  F600BC2D8F
  9C005AC2F8F0
  9C0141080250320F1802104A08
]

examples_p2.each do |str|
  print str.ljust(30), "\t"
  p read_packet(StringIO.new(parse(str))).val
end
=end

input_str = parse(File.read(filename))

pack = read_packet(StringIO.new(input_str))
puts "P1: #{pack.total_versions}"
puts "P2: #{pack.val}"
