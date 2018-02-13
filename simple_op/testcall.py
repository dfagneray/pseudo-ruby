import os 
import sys
import ast
import inspect
import astpretty

if(len(sys.argv) > 2):
	print("Too many arguments ! Specify only one file to parse")
else:
	f = sys.argv[1]
	f_ext = f[-3:]
	if(f_ext != ".rb"): print("Specify a ruby file !")
	else:
		name_ast = "parser_"+ f	
		r_ast = open(name_ast,"w")
		r_ast.write("require 'parser/current'\n")
		r_ast.write("Parser::Builders::Default.emit_lambda = true\n")
		r_ast.write("Parser::Builders::Default.emit_procarg0 = true\n")
		r_ast.write("cur_folder = Dir.pwd\n")
		r_ast.write("f =\"/"+f+"\"\n")
		r_ast.write("path = cur_folder + f\n")
		r_ast.write("code = File.read(path)\n")
		r_ast.write("ast = Parser::CurrentRuby.parse(code)\n")
		r_ast.write("p ast\n")
		r_ast.write("ast_"+f[0:-3]+"= File.new(\"ast_"+f[0:-3]+"\",\"w\")\n")
		r_ast.write("ast_"+f[0:-3]+".write(ast)\n")
		r_ast.write("ast_"+f[0:-3]+".close")
		r_ast.close()
