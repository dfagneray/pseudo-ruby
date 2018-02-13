require 'parser/current'
Parser::Builders::Default.emit_lambda = true
Parser::Builders::Default.emit_procarg0 = true
cur_folder = __dir__
f ="/simple.rb"
path = cur_folder + f
code = File.read(path)
ast = Parser::CurrentRuby.parse(code)
ast_simple= File.new(cur_folder+"/ast_simple","w")
ast_simple.write(ast)
ast_simple.close