import os
import sys
import filecmp
import yaml
import ruby_ast_translator
from Naked.toolshed.shell import execute_rb,muterun_rb
from subprocess import call

name = ["simple","simple_op","simple_list","simple_hash","simple_while","mid_while","mid_while_list","simple_for"]

#python3 -c 'import ruby_ast_translator; r = ruby_ast_translator.RubyASTTranslator(); r.Test()'
s = 0
for n in name:
	name_ast = n+"/parser_"+ n	+".rb"
	r_ast = open(name_ast,"w")
	r_ast.write("require 'parser/current'\n")
	r_ast.write("require 'ast'\n")
	r_ast.write("require 'sxp'\n")
	r_ast.write("Parser::Builders::Default.emit_lambda = true\n")
	r_ast.write("Parser::Builders::Default.emit_procarg0 = true\n")
	r_ast.write("Parser::Builders::Default.emit_encoding = true\n")
	r_ast.write("Parser::Builders::Default.emit_index = true\n")
	r_ast.write("def flatten_hash(hash)\n hash.each_with_object({}) do |(k,v), h|\n	if k.is_a? Hash\nflatten_hash(k).map do |h_k,h_v|\nif(h.include?(h_k))\nh[h_k].push(h_v)\nh[h_k] = h[h_k].flatten\n	else\nh[h_k] = h_v\nend\nend\nelse\nif(h.include?(k))\nh[k].push(v)\nh[k] = h[k].flatten\nelse\nh[k] = [v]\nend\nend\nend\nend\n")
	r_ast.write("def browse_acc(node,res,line,column)\nif (node == nil)\nreturn\nelsif (node.class == Parser::AST::Node)\ntemp = node.to_s\ntemp = temp.delete(' ')\ntemp = temp.delete(\"\n\")\ntemp= temp.delete('(')\ntemp = temp.delete(')')\nnode.children.each do |n|\nchild = n.to_s\nchild = child.delete(' ')\nchild = child.delete(\"\n\")\nchild = child.delete('(')\nchild = child.delete(')')\n	temp.slice!(child)\nend\nres[temp] = node.loc.line\nbrowse_acc(node.children,res,node.loc.line,node.loc.column)\nelsif (node.class == Array)\nnode.each do |n|\nif n.class == Parser::AST::Node\n		temp = {}\nbrowse_acc(n,temp,n.loc.line,n.loc.column)\nres[temp] = \"(\"+n.loc.line.to_s+\",\"+n.loc.column.to_s+\")\"\nelse\nres[n.to_s] = \"(\"+line.to_s+\",\"+column.to_s+\")\"\nend\nend\nelse\n	res[node.to_s] = \"(\"+line.to_s+\",\"+column.to_s+\")\"\nend\nend\n\ndef browse(node)\nres = {}\nbrowse_acc(node,res,-1,-1)\nreturn res\nend\n")
	r_ast.write("cur_folder = __dir__\n")
	r_ast.write("f =\"/"+n+".rb\"\n")
	r_ast.write("path = cur_folder + f\n")
	r_ast.write("code = File.read(path)\n")
	r_ast.write("ast = Parser::CurrentRuby.parse(code)\n")
	r_ast.write("res = browse(ast)\n")
	r_ast.write("res = flatten_hash(res).to_s.gsub! '=>',':'\n")
	r_ast.write("map_ast_"+n+" = File.new(cur_folder+\"/map_source_"+n+"\",\"w\")\n")
	r_ast.write("map_ast_"+n+".write(res)\n")
	r_ast.write("map_ast_"+n+".close\n")
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

r = ruby_ast_translator.RubyASTTranslator()
if s == len(name):
	for n in name:
		print("Beginning translation of "+n)
		try:
			r.Test(n)
		except:
			print("Problem with translation !")
	for n in name:
		try:
			f1 = open(n+"/"+n+".pseudo.yaml",'r')
		except:
			f1 = None
			print("Problem with pseudo-python file")
		try:
			f2 = open(n+".pseudo.yaml",'r')
		except:
			f2 = None
			print("Problem with created file")
		if f1 != None:
			y1 = yaml.load(f1)
		if f2 != None:
			y2 = yaml.load(f2)
		if(y1 == y2):
			print("Traduction of "+n+" succeeded")
		else:
			print("Traduction of "+n+" failed")
			print(set(y1)-set(y2))
		if(f1 != None and f2 != None):
			print(filecmp.cmp(n+"/"+n+".pseudo.yaml",n+".pseudo.yaml"))
		if f1 != None:
			f1.close()
		if f2 != None:
			f2.close()
	
