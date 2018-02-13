import os 
import sys
import ast
import yaml
import pyparsing

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

BUILTIN_FUNCTIONS = {'print', 'input', 'str', 'set', 'int', 'len', 'any', 'all', 'sum'}

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

class RubyASTTranslator:
	
	def translate(self):
		self.constants = []
		self.custom_exceptions = []
		self.definitions = []
		self.dependencies = []
		self.main = []
		self.ass_store = {}
	
	def translate_value(self,value):
		if(value[0] in BUILTIN_SIMPLE_TYPES):
			return self.translate_simple_value(value,value[0])
		elif(value[0] == 'array' or value[0] == 'hash'):
			return self.translate_nested_value(value)
		elif(value[0] == 'send'):
			return self.translate_send(value)
			
	
	def translate_simple_value(self,value,fr):
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
			elements = []
			t = ""
			for i in range(1,len(value)):
				if(isinstance(self.translate_value(value[i]),dict)):
					test = self.translate_value(value[i])
					if(t != "" and t != test['type']):
						return "In pseudo-Ruby, arrays can't have differents values"
					t = test['type']
					elements.append(test)
				else:
					test = self.translate_value(value[i])
					if(t != "" and t != test[0]):
						return "In pseudo-Ruby, arrays can't have differents values"
					t = test[1]
					elements.append(test)	
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
					return "In pseudo-Ruby, hash can't have differents values"
				t = self.translate_value(value[i][j])['type']
				pairs[i-1].append(self.translate_value(value[i][j]))
		return pairs,t			
	
	def translate_send(self,value):
		op = value[3]
		if(op in PSEUDO_OPS): 
			t = 'binary_op'
			left = self.ass_store[value[1][2]]
			right = self.translate_value(value[4])
		else:
			return "Operation not recognized"
		return{'left':left,'op':op,'pseudo_type':left['pseudo_type'],'right':right,'type':t}
	
	def translate_lvsagn(self,lv):
		print("---")
		print(lv[0])
		if(lv[0] == "begin"):
			i = 1
			while i<len(lv):
				self.translate_lvsagn(lv[i])
				i = i + 1
			return
		elif(lv[0] == "lvasgn"):
			name = lv[2]
			l_type = lv[3]
			if(l_type[0] in BUILTIN_TYPES or l_type[0] == "send"):
				ty = l_type[0]
			else:
				return "Type not recognized"
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
					self.main.append({'pseudo_type': 'Void','target':typ['left'],'type':'assignment','value':typ})
				else:
					target = {}
			if(target and target['name'] != None):
				self.ass_store[target['name']]=target
				self.main.append({'pseudo_type': 'Void','target':target,'type':'assignment','value':typ})
		else:
			return "Not an assignment bloc"
	
	def Test(self,name):
		self.translate()
		rel_path = name+"/ast_"+name
		path = os.path.dirname(__file__)
		with open(os.path.join(path,rel_path),"r") as fi:
			source = fi.read()	
		rast = source.replace('\n','')
		content_ast = pyparsing.Word(pyparsing.alphanums) | 'lvasgn' | ':' | 'int' | 'float' | 'begin' | 'array' | 'hash' | '-' | '+' | '/' | 'div' | '^' | '%'
		parenth = pyparsing.nestedExpr('(',')', content = content_ast)
		print(rast)
		res = parenth.parseString(rast)
		res = res.asList()
		print(len(res))
		print(res[0])
		self.main = []
		self.translate_lvsagn(res[0])
		print(self.main)
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
		

		