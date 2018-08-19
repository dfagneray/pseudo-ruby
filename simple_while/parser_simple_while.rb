require 'parser/current'
require 'ast'
require 'sxp'
Parser::Builders::Default.emit_lambda = true
Parser::Builders::Default.emit_procarg0 = true
Parser::Builders::Default.emit_encoding = true
Parser::Builders::Default.emit_index = true
def flatten_hash(hash)
 hash.each_with_object({}) do |(k,v), h|
	if k.is_a? Hash
flatten_hash(k).map do |h_k,h_v|
if(h.include?(h_k))
h[h_k].push(h_v)
h[h_k] = h[h_k].flatten
	else
h[h_k] = h_v
end
end
else
if(h.include?(k))
h[k].push(v)
h[k] = h[k].flatten
else
h[k] = [v]
end
end
end
end
def browse_acc(node,res,line,column)
if (node == nil)
return
elsif (node.class == Parser::AST::Node)
temp = node.to_s
temp = temp.delete(' ')
temp = temp.delete("
")
temp= temp.delete('(')
temp = temp.delete(')')
node.children.each do |n|
child = n.to_s
child = child.delete(' ')
child = child.delete("\n")
child = child.delete('(')
child = child.delete(')')
	temp.slice!(child)
end
res[temp] = res[temp] = "("+node.loc.line.to_s+","+node.loc.column.to_s+")"
browse_acc(node.children,res,node.loc.line,node.loc.column)
elsif (node.class == Array)
node.each do |n|
if n.class == Parser::AST::Node && n.loc.expression != nil
		temp = {}
browse_acc(n,temp,n.loc.line,n.loc.column)
res[temp] = "("+n.loc.line.to_s+","+n.loc.column.to_s+")"
else
res[n.to_s] = "("+line.to_s+","+column.to_s+")"
end
end
else
	res[node.to_s] = "("+line.to_s+","+column.to_s+")"
end
end

def browse(node)
res = {}
browse_acc(node,res,-1,-1)
return res
end
cur_folder = __dir__
f ="/simple_while.rb"
path = cur_folder + f
code = File.read(path)
ast = Parser::CurrentRuby.parse(code)
res = browse(ast)
res = flatten_hash(res).to_s.gsub! '=>',':'
map_ast_simple_while = File.new(cur_folder+"/map_source_simple_while","w")
map_ast_simple_while.write(res)
map_ast_simple_while.close
ast_simple_while= File.new(cur_folder+"/ast_simple_while","w")
ast_simple_while.write(ast)
ast_simple_while.close