import os 
import sys
import ast
import yaml
import pyparsing
import re
import errors

#python3 -c 'import ruby_ast_translator; r = ruby_ast_translator.RubyASTTranslator(); r.Test()'

EQUALS_BUILTIN_TYPES = {
	'array':	'list'
}

BUILTIN_TYPES = {
    'int':      'Int',
    'float':    'Float',
    'object':   'Object',
    'str':      'String',
    'array':	'List',
    'hash':     'Dictionary',
    'set':      'Set',
    'tuple':    'Tuple',
    'bool':     'Boolean',
    'SRE_Pattern': 'Regexp',
    'SRE_Match': 'RegexpMatch'
}

PSEUDON_BUILTIN_TYPES = {v: k for k, v in BUILTIN_TYPES.items()}

BUILTIN_SIMPLE_TYPES = {
    'int':      'Int',
    'float':    'Float',
    'str':      'String',
    'bool':     'Boolean'
}

KEY_TYPES = {'str', 'int', 'float', 'bool'}

PSEUDO_KEY_TYPES = {'String', 'Int', 'Float', 'Bool'}

BUILTIN_FUNCTIONS = {'print', 'set', 'int', 'length', 'any', 'all', 'sum','push','index'}

BUILTIN_TYPE_FUNCTIONS = {'length':'Int','push':'Void'}

FORBIDDEN_TOP_LEVEL_FUNCTIONS = {'map', 'filter'}

ITERABLE_TYPES = {'String', 'List', 'Dictionary', 'Set', 'Array'}

TESTABLE_TYPE = 'Boolean'

INDEXABLE_TYPES = {'String', 'List', 'Dictionary', 'Array', 'Tuple'}

COMPARABLE_TYPES = {'Int', 'Float', 'String'}

TYPES_WITH_LENGTH = {'String', 'List', 'Dictionary', 'Array', 'Tuple', 'Set'}

NUMBER_TYPES = {'Int', 'Float'}

PSEUDO_OPS = {
    '+': '+',
    '-': '-',
    '/': '/',
    '*': '*',
    '**': '**',

    '==': '==',
    '<': '<',
    '>': '>',
    '<=': '<=',
    '>=': '>=',
    '!=': '!=',
    
    '%': '%',

    'and': 'and',
    'or':  'or',
    'not': 'not',
    '&': '&',
    '|': '|',
    '^': '^'
}

PSEUDO_BINARY_OPS = {
    '+': '+',
    '-': '-',
    '/': '/',
    '*': '*',
    '**': '**',
    
    
    '%': '%'

}

PSEUDO_COMPARISON_OPS = {

	'==': '==',
    '<': '<',
    '>': '>',
    '<=': '<=',
    '>=': '>=',
    '!=': '!='

}

class RubyASTTranslator:
	
	def translate(self):
		self.constants = []
		self.custom_exceptions = []
		self.definitions = []
		self.dependencies = []
		self.main = []
		self.ass_store = {}
		self.source_loc = {}
		self.lines = []
		self.keyword = {}
	
	def translate_value(self,value):
		if value[0] in self.keyword:
			self.keyword[value[0]] = self.keyword[value[0]] + 1
		else:
			self.keyword[value[0]] = 0
		if(value[0] in BUILTIN_SIMPLE_TYPES):
			return self.translate_simple_value(value,value[0])
		elif(value[0] == 'array' or value[0] == 'hash'):
			return self.translate_nested_value(value)
		elif(value[0] == 'send'):
			return self.translate_send(value)
		elif(value[0] == 'while'):
			return self.translate_while(value)
		elif(value[0] == 'for'):
			if("irange" in value[2]):
				return self.translate_for_range(value)
			else:
				return self.translate_for(value)
			
	def is_terminal(self,value):
		if(isinstance(value,list) and value[2] in self.ass_store):
			return True
		else:
			return False
	def translate_simple_value(self,value,fr=None):
		if(fr == "array" or fr == "hash"):
			if(value[0] == 'int'):
				return [BUILTIN_TYPES[value[0]],{'pseudo_type':BUILTIN_TYPES[value[0]],'type':value[0],'value':int(value[1])}]
			elif(value[0] == 'float'):
				return [BUILTIN_TYPES[value[0]],{'pseudo_type':BUILTIN_TYPES[value[0]],'type':value[0],'value':float(value[1])}]
		else:
			if(value[0] == 'int'):
				return {'pseudo_type':BUILTIN_TYPES[value[0]],'type':value[0],'value':int(value[1])}
			elif(value[0] == 'float'):
				return {'pseudo_type':BUILTIN_TYPES[value[0]],'type':value[0],'value':float(value[1])}
	def translate_nested_value(self,value):		
		if(value[0] == 'array'):
			if(len(value) == 1):
				print(self.source_loc)
				loc = ast.literal_eval(self.source_loc[value[0]][self.keyword[value[0]]])
				meta = self.lines[loc[0]-2]
				if(meta[:6] == '#META:'):
					if(meta[6:10] == 'List' and meta[11:] in BUILTIN_SIMPLE_TYPES):
						return {'type': 'list', 'elements': [], 'pseudo_type': ['List', BUILTIN_SIMPLE_TYPES[meta[11:]]]}
					elif(meta[6:10] != 'List'):
						raise type_check_error('You put a meta comment before a list while it doesn\'t seem to concern a list',loc, self.lines[loc[0]-2])                
					elif(meta[11:] not in BUILTIN_SIMPLE_TYPES):
						raise type_check_error('The hinted type you gave is not supported for lists',loc, self.lines[loc[0]-2])
					else:
						raise type_check_error('pseudo-ruby needs you to hint the type when declaring empty list, with the syntax #META:List,<type>',loc, self.lines[loc[0]-1])
				else:
					raise type_check_error('pseudo-ruby needs you to hint the type when declaring empty list, with the syntax #META:List,<type>',loc, self.lines[loc[0]-1])
			print(value)
			elements = []
			t = ""
			for i in range(1,len(value)):
				if(isinstance(self.translate_value(value[i]),dict)):
					test = self.translate_value(value[i])
					if(t != "" and t != test['type']):
						raise type_check_error("In pseudo-Ruby, arrays can't have differents values")
					t = test['type']
					elements.append(test)
				else:
					test = self.translate_value(value[i])
					if(t != "" and t != test[0]):
						raise type_check_error("In pseudo-Ruby, arrays can't have differents values")
					t = test[1]
					elements.append(test)
			print(elements)
			print(t)
			return {'elements':elements,'pseudo_type': [BUILTIN_TYPES[value[0]],BUILTIN_TYPES[t]],'type': EQUALS_BUILTIN_TYPES[value[0]]}
		elif(value[0] == 'hash'):
			p,t = self.translate_pairs(value)
			pairs = []
			for pair in p:
				temp = {}
				temp['key'] = pair[0]
				temp['type'] = 'pair'
				temp['value'] = pair[1]
				pairs.append(temp)
			return {'pairs':pairs,'pseudo_type': [BUILTIN_TYPES[value[0]],BUILTIN_TYPES[t],BUILTIN_TYPES[t]],'type': 'dictionary'}
	def translate_pairs(self,value):
		pairs = [[] for _ in range(1,len(value))]
		for i in range(1,len(value)):
			t = ""
			for j in range(1,len(value[i])):
				if(t != "" and t != self.translate_value(value[i][j])['type']):
					raise type_check_error( "In pseudo-Ruby, hash can't have differents values")
				t = self.translate_value(value[i][j])['type']
				pairs[i-1].append(self.translate_value(value[i][j]))
		return pairs,t			
	
	def translate_send(self,value):
		op = value[3]
		if(op in PSEUDO_OPS): 
			if(op in PSEUDO_BINARY_OPS):
				t = 'binary_op'
			else:
				t = 'comparison'
			if(len(value[1])>2):
				left = self.ass_store[value[1][2]]
				if(left == None):
					raise type_check_error("Variable not assigned")
			else:
				left = self.translate_value(value[2])
			if(len(value[4])>2):
				if(isinstance(value[4][2],list)):
					if(value[4][0] == 'index'):
						right = self.translate_index(value)
					else:
						right = "hello"
				else:
					if (value[4][2]) in self.ass_store:
						right = self.ass_store[value[4][2]]
					else:
						right = self.translate_value(value[4])
				if(right == None):
					raise type_check_error("Variable not assigned")
			else:
				right = self.translate_value(value[4])
		elif (op in BUILTIN_FUNCTIONS):
			if(len(value[1])>2):
				left = self.ass_store[value[1][2]]
				if(left == None):
					raise type_check_error("Variable not assigned")
			else:
				left = self.translate_value(value[2])
			print("hello")
			print(value)
			if(self.is_terminal(value[1])):
				if(op in BUILTIN_TYPE_FUNCTIONS):
					typ = BUILTIN_TYPE_FUNCTIONS[op]
				else:
					typ = self.ass_store[value[1][2]]['pseudo_type'][1]
				print(typ)
				print(self.ass_store)
				if(len(value) < 5):
					return {'args':[],'message': op,'pseudo_type':typ,'type':'standard_method_call','receiver':self.ass_store[value[1][2]]}
				else:
					return {'args':[self.ass_store[value[4][2]]],'message': op,'pseudo_type':typ,'type':'standard_method_call','receiver':self.ass_store[value[1][2]]}
		else:
			raise type_check_error("Operation not recognized: "+op)
		if t == 'comparison':
			p_type = 'Boolean'
		else:
			p_type = left['pseudo_type']
		return{'left':left,'op':op,'pseudo_type':p_type,'right':right,'type':t}
	
	def translate_index(self,value):
		index = self.ass_store[value[4][2][2]]
		ps = index['pseudo_type']
		sequence = self.ass_store[value[4][1][2]]
		return {'index':index,'pseudo_type':ps,'sequence':sequence,'type':'index'}
	
	def translate_length(self,value):
		print()
		
	
	def translate_while(self,value):
		i = 1
		block = []
		while i<len(value):
			print("---")
			print(value[i])
			block = self.translate_assign(value[i])
			print(self.translate_assign(value[i]))
			i = i + 1
		if(not isinstance(block,list)):
			block = [block]
		return {'block':block,'pseudo_type':'Void','test':self.translate_value(value[1]),'type':'while_statement'}
	def translate_for_range(self,value):
		i = 1
		block = []
		while i < len(value):
			block.append(self.translate_assign(value[i]))
			i = i + 1
		if(not isinstance(block,list)):
			block = [block]
		return {'block':block[2:],'end':block[1][0],'index':block[0],'step':block[1][2],'start':block[1][1],'pseudo_type':'Void','type':'for_range_statement'}
		
	def translate_for(self,value):
		i = 1
		block = []
		while i < len(value):
			block.append(self.translate_assign(value[i],"for_statement"))
			i = i + 1
		if(not isinstance(block,list)):
			block = [block]
		return {'block':[block[1]],'iterators':{'iterator':block[0],'type':'for_iterator'},'pseudo_type':'Void','sequences':{'sequence':self.ass_store[value[2][3]],'type':'for_sequence'},'type':'for_statement'}
	
	def translate_assign(self,lv,fr = None):
		if lv[0] in self.keyword:
			self.keyword[lv[0]] = self.keyword[lv[0]] + 1
		else:
			self.keyword[lv[0]] = 0
		if(lv[0] == "begin"):
			i = 1
			b = []
			while i<len(lv):
				b.append(self.translate_assign(lv[i],fr))
				i = i + 1
			return b
		elif(lv[0] == "lvasgn"):
			if(len(lv)==3):
				self.ass_store[lv[2]]={'name':lv[2], 'pseudo_type':'Int','type':'local'} #Maybe not assume type here..
				return {'name':lv[2], 'pseudo_type':'Int','type':'local'}
			name = lv[2]
			l_type = lv[3]
			if(l_type[0] in BUILTIN_TYPES or l_type[0] == "send"):
				ty = l_type[0]
			elif(l_type[0] in PSEUDO_OPS):
				return self.translate_send(lv)
			else:
				raise type_check_error("Type not recognized")
			typ = self.translate_value(l_type)
			if(ty in BUILTIN_SIMPLE_TYPES):
				target = {'name':name, 'pseudo_type':BUILTIN_TYPES[ty],'type':'local'}
			else:
				if(ty == 'array'):
					target = {'name':name, 'pseudo_type':typ['pseudo_type'],'type':'local'}
				elif(ty == 'hash'):
					target = {'name':name, 'pseudo_type':typ['pseudo_type'],'type':'local'}
				elif(ty == 'send'):
					target = {'name':name, 'pseudo_type':typ['pseudo_type'],'type':'local'}
					if(target and target['name'] != None):
						self.ass_store[target['name']]=target
					return{'pseudo_type': 'Void','target':target,'type':'assignment','value':typ}
				else:
					target = {}
			if(target and target['name'] != None):
				self.ass_store[target['name']]=target
				return{'pseudo_type': 'Void','target':target,'type':'assignment','value':typ}
		elif(lv[0] == "irange"):
			return [self.translate_simple_value(lv[2]),self.translate_simple_value(lv[1]),self.translate_simple_value(['int','1'])]
		elif(lv[0] == "send" and fr == "for_statement"):
			return self.translate_assign(lv[4][1][2])
		elif(lv[0] == "send"):
			return self.translate_send(lv)
		elif(lv[0] == "return"):
			return self.translate_return(lv)
		else:
			print("xx")
			print(lv)
	
	def translate_return(self,lv):
		val = self.ass_store[lv[1][2]]
		return {'pseudo_type':val['pseudo_type'],'type':'implicit_return','value':val}
	
	def translate_kwoptarg(self,lv):
		arg = {'name':lv[2],'pseudo_type':BUILTIN_TYPES[lv[3][3]],'type':'local'}
		self.ass_store[lv[2]] = arg
		return arg	
	
	def translate_args(self,lv):
		args = []
		if len(lv) > 1:
			i = 1
			while i<len(lv):
				if(lv[i][0] == "kwoptarg"):
					args.append(self.translate_kwoptarg(lv[i]))
				i = i + 1
		return args
			
	def translate_lvsagn(self,lv,options=None):
		print("----")
		print(lv)
		if lv[0] in self.keyword:
			self.keyword[lv[0]] = self.keyword[lv[0]] + 1
		else:
			self.keyword[lv[0]] = 0
		if(lv[0] == "begin"):
			i = 1
			res = []
			while i<len(lv):
				res.append(self.translate_lvsagn(lv[i],options))
				i = i + 1
			return res
		elif(lv[0]=="class"):
			print("class")
			print(lv)
			name = lv[1][3]
			methods = self.translate_lvsagn(lv[3],name)
			cons = None
			meth = []
			for m in methods:
				if m['type'] == 'constructor':
					cons = m
				elif m['type'] == 'function_definition':
					meth.append(m)
			self.definitions.append({'attrs':None,'name':name,'base':None,'constructor':cons,'methods':meth,'type':'class_definition'})
		elif(lv[0]== "def"):
			name = lv[2]
			print("DEF")
			print(name)
			r_t = 'Void'
			#self.func_store[{'name':name,'return_type':r_t}]
			params = self.translate_args(lv[3])
			print(params)
			#print(self.ass_store[lv[-1][-1][1][2]])
			p_t = ['Function']
			for p in params:
				p_t.append(p['pseudo_type'])
			block = self.translate_assign(lv[4],options)
			if(name != 'initialize' and block[-1]['type']):
				r_t = block[-1]['pseudo_type']
			p_t.append(r_t)
			if not p_t:
				p_t = 'Void'
			if (name == 'initialize'):
				print('initialize')
				return {'name':'__init__','block':None,'params':None,'return_type':r_t,'pseudo_type':'Void','this':{'name':options,'type':'typename'},'type':'constructor'}
			if options:
				return {'params':params,'name':name,'pseudo_type':p_t,'return_type':r_t,'type':'function_definition','block':block,'this':{'name':options,'type':'typename'},'is_public':False}
			else:
				self.definitions.append({'params':params,'name':name,'pseudo_type':p_t,'return_type':r_t,'type':'function_definition','block':block})
		elif(lv[0] == "lvasgn"):
			name = lv[2]
			l_type = lv[3]
			if(l_type[0] in BUILTIN_TYPES or l_type[0] == "send"):
				ty = l_type[0]
			else:
				raise type_check_error("Type not recognized")
			typ = self.translate_value(l_type)
			if(ty in BUILTIN_SIMPLE_TYPES):
				target = {'name':name, 'pseudo_type':BUILTIN_TYPES[ty],'type':'local'}
			else:
				if(ty == 'array'):
					target = {'name':name, 'pseudo_type':typ['pseudo_type'],'type':'local'}
				elif(ty == 'hash'):
					target = {'name':name, 'pseudo_type':typ['pseudo_type'],'type':'local'}
				elif(ty == 'send'):
					target = {}
					print(typ)
					self.main.append({'pseudo_type': 'Void','target':typ['left'],'type':'assignment','value':typ})
				else:
					target = {}
			if(target and target['name'] != None):
				self.ass_store[target['name']]=target
				self.main.append({'pseudo_type': 'Void','target':target,'type':'assignment','value':typ})
		elif(lv[0] == "while"):
			self.main.append(self.translate_value(lv))
		elif(lv[0] == 'for'):
			self.main.append(self.translate_value(lv))
		else:
			raise errors.type_check_error("Not an assignment bloc")
	
	def Test(self,name):
		self.translate()
		rel_ast_path = name+"/ast_"+name
		rel_source_path = name+"/"+name+".rb"
		path = os.path.dirname(__file__)
		with open(os.path.join(path,rel_ast_path),"r") as fi:
			ast_source = fi.read()	
		with open(os.path.join(path,rel_source_path),"r") as fi:
			source = fi.read()
		self.lines = source.splitlines()
		test_path = name+"/map_source_"+name
		with open(os.path.join(path,test_path),"r") as fi:
			source_loc = fi.read()
		self.source_loc = ast.literal_eval(source_loc)
		rast = ast_source.replace('\n','')
		content_ast = pyparsing.Word(pyparsing.alphanums) | 'ivasgn' | 'class' | 'lvasgn' | ':' | 'int' | 'float' | 'begin' | 'array' | 'hash' | '-' | '+' | '/' | 'div' | '^' | '%' | '<' | '>' | '==' | '<=' | '>=' | '!=' | 'push' | '[' | ']' | 'Array' | 'new' | 'const' | 'length' | 'nil' | '[]' | '*' | 'def' | '{' | '}' | '{}' | '@'
		print(content_ast)
		parenth = pyparsing.nestedExpr(opener ='(',closer =')', content = content_ast)
		res = parenth.parseString(rast)
		res = res.asList()
		print("res")
		print(res)
		self.main = []
		self.translate_lvsagn(res[0])
		print(self.main)
		print(res)	
		trad = {'constants':self.constants,'custom_exceptions':self.custom_exceptions,'definitions':self.definitions,'dependencies':self.dependencies,'main':self.main,'type':'module'}
		fil = open(name + '.pseudo.yaml','w')
		noaliases = yaml.dumper.SafeDumper
		noaliases.ignore_aliases = lambda self, data: True
		fil.write(yaml.dump(trad,Dumper = noaliases))
		fil.close()
if __name__ == '__main__':
	argc = len(sys.argv)
	argv = sys.argv
	if argc == 2:
		r = RubyASTTranslator()
		r.Test(argv[1])
		

		
