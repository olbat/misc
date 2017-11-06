require 'benchmark'

n=1_000_000
str1="Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum"
str2="Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of lorem Ipsum"

Benchmark.bm do |x|
  x.report('casecmp ') { i=0; n.times{ i+=1 if str1.casecmp(str2) != 0 }; p i }
  x.report('downcase== ') { i=0; n.times{ i+=1 if str1.downcase == str2.downcase }; p i }
  x.report('regexp ') { i=0; n.times{ i+=1 if str1.match(/#{str2}/i)}; p i }
end
