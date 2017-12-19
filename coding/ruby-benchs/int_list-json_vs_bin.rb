require 'json'
require 'stringio'

NUM_DOCS = 10000
NUM_WEIGHTS = 300
BUFF_SIZE=1000
BYTESIG='Test'

puts "docs:#{NUM_DOCS} weights:#{NUM_WEIGHTS}"

bin_format = "L#{'f' * NUM_WEIGHTS}"

# bin format: ID_SIZE(int) + NUM_WEIGHTS(int) then id#(str) + weights(float)
# (save ID_SIZE and NUM_WEIGHTS as first entry to be more dynamic)
bin = StringIO.new
json = StringIO.new

# Test size

# write NUM_WEIGHTS(uint32) (4 bytes)
bin.write(BYTESIG)
bin.write([NUM_WEIGHTS].pack('L'))

NUM_DOCS.times do |n|
  v = [n] # doc "id"
  NUM_WEIGHTS.times{ v << rand() }

  bin.write(v.pack(bin_format))
  json.write(v.to_json << "\n")
end

puts "  bin size:\t#{bin.string.bytesize}"
puts "  json size:\t#{json.string.bytesize}"


# Test parse time

bin.rewind
ret = []
startt = Time.now

# check byte signature
abort 'invalid binary format' unless bin.read(BYTESIG.bytesize) == BYTESIG

# read NUM_WEIGHTS(uint32) (4 bytes)
num_weights = bin.read(4).unpack('L').first
bin_format = "L#{'f' * num_weights}"
bin_size = 4 + (num_weights * 4) # sizeof(uint32) + num_weights * sizeof(Float)

until bin.eof? do
  # Simple version
  ret << bin.read(bin_size).unpack(bin_format)

  # Buffered version
  #buff = bin.read(BUFF_SIZE * bin_size)
  #(buff.bytesize / bin_size).times do |n|
  #  ret << buff[(n*bin_size)..(((n+1)*bin_size)-1)].unpack(bin_format)
  #end
end
puts "  bin parse time: #{Time.now - startt}"

json.rewind
ret = []
startt = Time.now
json.each{|s| ret << JSON.parse(s) }
puts "  json parse time: #{Time.now - startt}"
