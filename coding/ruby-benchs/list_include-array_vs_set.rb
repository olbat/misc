require 'benchmark'
require 'set'

data_array = Hash.new{|h, k| h[k] = [] }
data_set = Hash.new{|h, k| h[k] = Set.new }

min_pow = (ARGV.size > 0 ? ARGV[0].to_i : 0)
max_pow = (ARGV.size > 1 ? ARGV[1].to_i : 16)
# prepare data : 100 values for each size from 2^min_pow to 2^max_pow
File.open('/dev/urandom', 'rb') do |file|
  10_000.times do
    (min_pow..max_pow).map{|v| 2**v.to_i }.each do |size|
      data = file.read(size)
      data_array[size] << data
      data_set[size] << data
    end
  end
end

Benchmark.bm(20) do |bench|
  data_array.each do |size, values|
    bench.report("array / #{size}") do
      values.each{|value| values.include?(value) }
    end
  end
  data_set.each do |size, values|
    bench.report("set / #{size}") do
      values.each{|value| values.include?(value) }
    end
  end
end
