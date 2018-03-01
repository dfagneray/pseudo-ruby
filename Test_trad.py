import os
import sys
import filecmp
import yaml
import ruby_ast_translator
from Naked.toolshed.shell import execute_rb,muterun_rb
from subprocess import call

name = ["simple","simple_op","simple_list","simple_hash","simple_while","mid_while","simple_for","simple_for_each"]

#python3 -c 'import ruby_ast_translator; r = ruby_ast_translator.RubyASTTranslator(); r.Test()'
s = 0
for n in name:
	name_ast = n+"/parser_"+ n	+".rb"
	r_ast = open(name_ast,"w")
	r_ast.write("require 'parser/current'\n")
	r_ast.write("Parser::Builders::Default.emit_lambda = true\n")
	r_ast.write("Parser::Builders::Default.emit_procarg0 = true\n")
	r_ast.write("cur_folder = __dir__\n")
	r_ast.write("f =\"/"+n+".rb\"\n")
	r_ast.write("path = cur_folder + f\n")
	r_ast.write("code = File.read(path)\n")
	r_ast.write("ast = Parser::CurrentRuby.parse(code)\n")
	r_ast.write("ast_"+n+"= File.new(cur_folder+\"/ast_"+n+"\",\"w\")\n")
	r_ast.write("ast_"+n+".write(ast)\n")
	r_ast.write("ast_"+n+".close")
	r_ast.close()
	print(os.getcwd()+"/"+n+"/parser_"+n+".rb")
	success = execute_rb(os.getcwd()+"/"+n+"/parser_"+n+".rb")
	if(success):
		print("Parser created successfully for "+n+" and file parsed !")
		s = s + 1
	else:
		print("Problem with creation of parser")

if s == len(name):
	for n in name:
		r = ruby_ast_translator.RubyASTTranslator()
		r.Test(n)
	for n in name:
		f1 = open(n+"/"+n+".pseudo.yaml",'r')
		f2 = open(n+".pseudo.yaml",'r')
		y1 = yaml.load(f1)
		y2 = yaml.load(f2)
		if(y1 == y2):
			print("Traduction of "+n+" succeeded")
		else:
			print("Traduction of "+n+" failed")
			print(set(y1)-set(y2))
		print(filecmp.cmp(n+"/"+n+".pseudo.yaml",n+".pseudo.yaml"))
		f1.close()
		f2.close()
	
