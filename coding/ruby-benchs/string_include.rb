require 'benchmark'

n=1_000_000
str_short="Lorem Ipsum is simply dummy text of the printing and typesetting industry."
str_long="Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum"

Benchmark.bm do |x|
  x.report('include/short') { i=0; n.times{ i+=1 if str_short.include?('.') != 0 }; p i }
  x.report('regexp/short') { i=0; n.times{ i+=1 if str_short.match(/\./)}; p i }
  x.report('include/long') { i=0; n.times{ i+=1 if str_long.include?('.') != 0 }; p i }
  x.report('regexp/long') { i=0; n.times{ i+=1 if str_long.match(/\./)}; p i }
end
