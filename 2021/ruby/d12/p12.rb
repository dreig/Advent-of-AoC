require "debug"
filename = ARGV[0]

@mapping = {}
@edges   = []
@isSmall = []

def registerVertex(name)
  @mapping.fetch(name) do
    @edges.push []
    @isSmall.push(name == name.downcase)
    (@edges.size-1).tap do |num|
      @mapping[name] = num
      @start = num if name == "start"
      @end = num if name == "end"
    end
  end
end

File.foreach(filename) do |line|
  line.strip!
  break if line == ""
  a, b = line.split('-').map(&:strip).map { registerVertex(_1) }
  @edges[a].push(b)
  @edges[b].push(a)
end

@N = @isSmall.size

def explore(node)
  if node == @end
    @paths_count += 1
    return
  end

  for nbr in @edges[node]
    next if @vis[nbr] >= @current_limit

    if @isSmall[nbr]
      @vis[nbr] += 1
      if @vis[nbr] == @limit && @extra_left > 0
        @extra_left -= 1
        @current_limit -= 1
      end
    end

    explore(nbr)

    if @isSmall[nbr]
      if @vis[nbr] == @limit && @current_limit < @limit
        @extra_left += 1
        @current_limit += 1
      end
      @vis[nbr] -= 1
    end
  end
end

def setup_p1
  @paths_count = 0
  @vis = Array.new(@N, 0)
  @current_limit = @limit = 1
  @extra_left = 0
  @vis[@start] = 1
end

def setup_p2
  @paths_count = 0
  @vis = Array.new(@N, 0)
  @current_limit = @limit = 2
  @extra_left = 1
  @vis[@start] = 2
end

setup_p1
explore(@start)
puts "P1: #{@paths_count}"

setup_p2
explore(@start)
puts "P2: #{@paths_count}"
