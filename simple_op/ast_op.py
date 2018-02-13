import ast

tree = ast.parse("i = 5;j = j - 1")
print(ast.dump(tree))
