require 'parser/current'
Parser::Builders::Default.emit_lambda = true
Parser::Builders::Default.emit_procarg0 = true
cur_folder = __dir__
f ="/simple_op.rb"
path = cur_folder + f
code = File.read(path)
ast = Parser::CurrentRuby.parse(code)
ast_simple_op= File.new(cur_folder+"/ast_simple_op","w")
ast_simple_op.write(ast)
ast_simple_op.close