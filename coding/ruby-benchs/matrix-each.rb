require 'benchmark'

SIZE = 10_000

m = Array.new(SIZE){ Array.new(SIZE){ rand(2) } }

Benchmark.bm(20) do |b|
  b.report("double .size.times") do
    count = 0
    m.size.times do |i|
      m[i].size.times do |j|
        count += 1 if m[i][j] == 0
      end
    end
    p count
  end

  b.report("double .each") do
    count = 0
    m.each do |n|
      n.each do |v|
        count += 1 if v == 0
      end
    end
    p count
  end

  b.report(".inject + .count") do
    p m.inject(0){|sum, n| sum + n.count{|v| v == 0 } }
  end
end
