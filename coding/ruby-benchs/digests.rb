require 'benchmark'
require 'digest'

data = Hash.new{|h,k| h[k] = [] }
min_pow = (ARGV.size > 0 ? ARGV[0].to_i : 0)
max_pow = (ARGV.size > 1 ? ARGV[1].to_i : 16)
# prepare data : 100 values for each size from 2^min_pow to 2^max_pow
File.open('/dev/urandom', 'rb') do |file|
  10_000.times do
    (min_pow..max_pow).map{|v| 2 ** v.to_i}.each do |size|
      data[size] << file.read(size)
    end
  end
end

digests = [
  Digest::MD5,
  Digest::SHA1,
  Digest::SHA2,
  Digest::SHA256,
  Digest::SHA384,
  Digest::SHA512
]

Benchmark.bmbm(20) do |bench|
  data.each do |size, values|
    digests.each do |digest|
      bench.report("#{size} / #{digest.name}") do
        values.each{ |value| digest.hexdigest(value) }
      end
    end
  end
end
