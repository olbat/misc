require 'benchmark'

def ngram_each_cons(tokens, win)
  tokens.each_cons(win).to_a
end

def ngram_while(tokens, win)
  ret = []
  pos = 0
  while pos <= tokens.size - win
    ret << tokens[pos...pos + win].join(' ')
    pos += 1
  end
  ret
end

def ngram_while_blk(tokens, win)
  pos = 0
  while pos <= tokens.size - win
    yield tokens[pos...pos + win].join(' ')
    pos += 1
  end
end

text = STDIN.read.split("\n")

Benchmark.bm(34) do |b|
  2.upto(6) do |size|
    b.report("size:#{size},ngram:each_cons,split:str") do
      text.each{|l| ngram_each_cons(l.split(" "), size) }
    end
    b.report("size:#{size},ngram:while,split:str") do
      text.each{|l| ngram_while(l.split(" "), size){} }
    end
    b.report("size:#{size},ngram:while_blk,split:str") do
      text.each{|l| ngram_while_blk(l.split(" "), size){} }
    end
    b.report("size:#{size},ngram:each_cons,split:regexp") do
      text.each{|l| ngram_each_cons(l.split(/\s+/), size) }
    end
    b.report("size:#{size},ngram:while,split:regexp") do
      text.each{|l| ngram_while(l.split(/\s+/), size){} }
    end
    b.report("size:#{size},ngram:while_blk,split:regexp") do
      text.each{|l| ngram_while_blk(l.split(/\s+/), size){} }
    end
  end
end
