require 'parser/current'
Parser::Builders::Default.emit_lambda = true
Parser::Builders::Default.emit_procarg0 = true
cur_folder = __dir__
f ="/simple_for_each.rb"
path = cur_folder + f
code = File.read(path)
ast = Parser::CurrentRuby.parse(code)
map_ast_simple_for_each = File.new(cur_folder+"/map_ast_simple_for_each","w")
ast.children.each do |c|
	 if c.class == Parser::AST::Node
	 	map_ast_simple_for_each.write(c.to_sexp + ":"+c.loc.line.to_s+"\n")
	 end
end
map_ast_simple_for_each.close
ast_simple_for_each= File.new(cur_folder+"/ast_simple_for_each","w")
ast_simple_for_each.write(ast)
ast_simple_for_each.close