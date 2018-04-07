require 'parser/current'
Parser::Builders::Default.emit_lambda = true
Parser::Builders::Default.emit_procarg0 = true
cur_folder = __dir__
f ="/simple_op.rb"
path = cur_folder + f
code = File.read(path)
ast = Parser::CurrentRuby.parse(code)
map_ast_simple_op = File.new(cur_folder+"/map_ast_simple_op","w")
p ast
ast.children.each do |c|
p c.class
map_ast_simple_op.write(c.to_sexp + ":"+c.loc.line.to_s+"\n")
end
map_ast_simple_op.close
ast_simple_op= File.new(cur_folder+"/ast_simple_op","w")
ast_simple_op.write(ast)
ast_simple_op.close
