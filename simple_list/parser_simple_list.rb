require 'parser/current'
Parser::Builders::Default.emit_lambda = true
Parser::Builders::Default.emit_procarg0 = true
cur_folder = __dir__
f ="/simple_list.rb"
path = cur_folder + f
code = File.read(path)
ast = Parser::CurrentRuby.parse(code)
ast_simple_list= File.new(cur_folder+"/ast_simple_list","w")
ast_simple_list.write(ast)
ast_simple_list.close