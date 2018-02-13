import yaml

with open('doubleodds.pseudo.yaml','r') as stream:
	try:
		y = yaml.load(stream)
	except yaml.YAMLError as exc:
		print(exc)
		

for i in y['main']:
	print(i)
