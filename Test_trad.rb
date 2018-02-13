require 'rubygems'
require 'yaml'
require 'pp'

l1 = "simple_list.pseu"
l2 = "simple_list/simple_list.pseudo"
first = YAML.load_file(l1+".yaml")
second = YAML.load_file(l2+".yaml")



def diff(root, compared, structure = [])
  root.each_key do |key|
    next_root     = root[key]
    next_compared = compared.nil? ? nil : compared[key]
    new_structure = structure.dup << key
    puts "#{new_structure.join(".")}" if compared.nil? || compared[key].nil?
    diff(next_root, next_compared, new_structure) if next_root.kind_of? Hash
  end
end

h1 = diff(first, second, [])
h2 = diff(second, first, [])

puts(h1.to_a)
puts(h2.to_a)
puts("\n")

if(h1.size > h2.size)
	difference = h1.to_a - h2.to_a
else
	difference = h2.to_a - h1.to_a
end

puts(Hash[*difference.flatten])
