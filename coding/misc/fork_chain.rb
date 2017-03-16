#!/usr/bin/ruby

# This program runs a method several times on different processus in an
# ordered way creating a chain using fork and pipes

# Example of a pipe chain with 4 children:
#
# main-----------------,
#     ,-[r|pipe#0|w]<--'
#     '---------------, child#1
#     ,-[r|pipe#1|w]<-'
#     '---------------, child#2
#     ,-[r|pipe#2|w]<-'
#     '---------------, child#3
#     ,-[r|pipe#3|w]<-'
#     '---------------, child#4
#    ,--[r|pipe#4|w]<-'
# main

# The processing method to be redefined
def process(i)
  puts i
end

# Spawns a child and run the processing method
def spawn_child(firstp, prevp, curp)
  # children have to process in order so each child wait for the prev. child
  # by reading in a pipe and notify the next one by writing in another pipe
  fork do
    # always close the write end of the first pipe in children since it's only
    # used by the main process
    firstp[:w].close

    # close the read end of the current pipe
    # (will be used by the next child)
    curp[:r].close

    # read (wait) value from the the previous pipe
    val = Marshal.load(prevp[:r].read)
    prevp[:r].close

    # increment val and run the processing method
    val += 1
    process(val)

    # write it to the current pipe
    curp[:w].write(Marshal.dump(val))
    curp[:w].close
  end
end


# Main program
chain_size = (ARGV.size >= 1 && ARGV[0] =~ /^\d+$/ ? ARGV[0].to_i : 8)
firstp = prevp = Hash[[:r, :w].zip(IO.pipe)]
children_pids = []

# write end of prevp is not closed when n == 0 since the main process will
# write in the pipe
chain_size.times do |n|
  curp = Hash[[:r, :w].zip(IO.pipe)]
  children_pids << spawn_child(firstp, prevp, curp)
  # close the write end of the current pipe (only used by children)
  curp[:w].close
  # read end of prevp is not closed when n == (num-1) since the main process
  # will read from the pipe
  prevp[:r].close if n != (chain_size - 1)
  prevp = curp
end

# write to the first pipe of the chain
firstp[:w].write(Marshal.dump(0))
firstp[:w].close

# read from the last pipe of the chain
prevp[:r].read
prevp[:r].close

# wait for children
children_pids.each{|pid| Process.waitpid(pid) }
