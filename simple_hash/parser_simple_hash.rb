require 'parser/current'
Parser::Builders::Default.emit_lambda = true
Parser::Builders::Default.emit_procarg0 = true
cur_folder = __dir__
f ="/simple_hash.rb"
path = cur_folder + f
code = File.read(path)
ast = Parser::CurrentRuby.parse(code)
ast_simple_hash= File.new(cur_folder+"/ast_simple_hash","w")
ast_simple_hash.write(ast)
ast_simple_hash.close