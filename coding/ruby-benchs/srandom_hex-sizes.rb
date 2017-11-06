require 'benchmark'
require 'securerandom'

n=10_000_000

Benchmark.bm do |x|
  x.report('size 2') { n.times{ SecureRandom.hex(2) } }
  x.report('size 4') { n.times{ SecureRandom.hex(4) } }
  x.report('size 8') { n.times{ SecureRandom.hex(8) } }
  x.report('size 12') { n.times{ SecureRandom.hex(12) } }
  x.report('size 16') { n.times{ SecureRandom.hex(16) } }
  x.report('default') { n.times{ SecureRandom.hex() } }
end
