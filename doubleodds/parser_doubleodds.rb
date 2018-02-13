require 'parser/current'
require 'ast'

BUILTIN_TYPES = {
    'int'=>     'Int',
    'float'=>    'Float',
    'object'=>   'Object',
    'str'=>      'String',
    'list'=>     'List',
    'dict'=>     'Dictionary',
    'set'=>      'Set',
    'tuple'=>    'Tuple',
    'bool'=>     'Boolean',
    'SRE_Pattern'=> 'Regexp',
    'SRE_Match'=> 'RegexpMatch'
}

BUILTIN_SIMPLE_TYPES = {
    'int'=>      'Int',
    'float'=>    'Float',
    'str'=>      'String',
    'bool'=>     'Boolean'
}


KEY_TYPES = ['str', 'int', 'float', 'bool']

PSEUDO_KEY_TYPES = ['String', 'Int', 'Float', 'Bool']

BUILTIN_FUNCTIONS = ['p', 'input', 'str', 'set', 'int', 'length', 'any', 'all']#check builtin function for ruby

FORBIDDEN_TOP_LEVEL_FUNCTIONS = ['map', 'filter']

ITERABLE_TYPES = ['String', 'List', 'Dictionary', 'Set', 'Array']

TESTABLE_TYPE = 'Boolean'

INDEXABLE_TYPES = ['String', 'List', 'Dictionary', 'Array', 'Tuple']

COMPARABLE_TYPES = ['Int', 'Float', 'String']

TYPES_WITH_LENGTH = ['String', 'List', 'Dictionary', 'Array', 'Tuple', 'Set']#check if Set and Tuple are built the same way in ruby

NUMBER_TYPES = ['Int', 'Float']

PSEUDO_OPS = {
    'Add'=> '+',
    'Sub'=> '-',
    'Div'=> '/',
    'Mult'=> '*',
    'Pow'=> '**',

    'Eq'=> '==',
    'Lt'=> '<',
    'Gt'=> '>',
    'LtE'=> '<=',
    'GtE'=> '>=',
    'NotEq'=> '!=',
    'Mod'=> '%',

    'And'=> 'and',
    'Or'=>  'or',
    'Not'=> 'not',
    'BitAnd'=> '&',
    'BitOr'=> '|',
    'BitXor'=> '^'
}


Parser::Builders::Default.emit_lambda = true
Parser::Builders::Default.emit_procarg0 = true
cur_folder = Dir.pwd
f ="/doubleodds.rb"
path = cur_folder + f
code = File.read(path)
ast = Parser::CurrentRuby.parse(code)
ast_doubleodds= File.new("ast_doubleodds","w")
ast_doubleodds.write(ast)
ast_doubleodds.close

child = ast.children



