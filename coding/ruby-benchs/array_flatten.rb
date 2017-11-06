require 'benchmark'

Benchmark.bm(34) do |b|
  1.upto(10) do |size|
    arr = (10**size).times.to_a

    b.report("size:#{arr.size}, .map.flatten(1)") do
      arr.map{|v| v.times.to_a }.flatten(1)
    end

    b.report("size:#{arr.size}, .flat_map") do
      arr.flat_map{|v| v.times.to_a }
    end

    b.report("size:#{arr.size}, .map.each") do
      a = arr.map{|v| v.times.to_a }
      r = []
      a.each{|v| r.concat(v) }
    end

    b.report("size:#{arr.size}, .each") do
      r = []
      arr.each{|v| r.concat(v.times.to_a) }
    end
  end
end
