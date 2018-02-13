require 'parser/current'
Parser::Builders::Default.emit_lambda = true
Parser::Builders::Default.emit_procarg0 = true
cur_folder = __dir__
f ="/simple_while.rb"
path = cur_folder + f
code = File.read(path)
ast = Parser::CurrentRuby.parse(code)
ast_simple_while= File.new(cur_folder+"/ast_simple_while","w")
ast_simple_while.write(ast)
ast_simple_while.close