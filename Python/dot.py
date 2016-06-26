"""

Parser for a (slightly modified) version of the DOT language.
DOT was designed by Emden Gansner and Stephen North at AT&T Research Labs as part of the Graphviz suite.
This modified version of the language is lacking in most of the advanced features, but just enough for
nodes to be labeled and organized in undirected and directed graphs.


"""
a = ["digraph graphname {",
		"i_1 -> sigma",
		"i_2 -> sigma",
		"i_3 -> sigma",
		"sigma -> step",
		"step -> output",
	"}"]
b = ["graph graphname {",
		"NSA -- IC",
		"CIA -- IC",
		"DIA -- IC",
		"NGA -- IC",
		"DHS -- IC",
		"DOE -- IC",
		"NASIC -- IC",
	"}"]

c = ["graph graphname {",
"run -- intr",
"intr -- runbl",
"runbl -- run",
"run -- kernel",
"kernel -- zombie",
"kernel -- sleep",
"kernel -- runmem",
"sleep -- swap",
"swap -- runswap",
"runswap -- new",
"runswap -- runmem",
"new -- runmem",
"sleep -- runmem",
"}"]

graphSchema = {"edges":[]}
digraphSchema = {"to": [],"from":[]}
def parseGraph(g,meta):
	graph = [[]]
	ind = 0
	fin = []
	d = [[]]
	dg = {}
	for item in g:
		if item[len(item)-2:] != '!n':
			graph[ind].append(item)
		else:
			graph[ind].append(item[:len(item)-2])
			ind += 1
			graph.append([])

	for edge in graph:
		for node in edge:
			if node != ('->' if meta[0] == 'digraph' else '--'):
				dg[node] = []
	for edge in graph:
		if len(edge) != 0:
			dg[edge[0]].append(edge[2])
			if meta[0] == 'graph':
				dg[edge[2]].append(edge[0])

	return {'type': meta[0], 'name': meta[1], 'edges': dg}
	#print graph

def parseDot(dot):
	dotArr = '!n '.join(dot).split(' ')
	graph = dotArr[3:len(dotArr)-1]
	meta = [dotArr[0],dotArr[1]]
	return parseGraph(graph,meta)

def toDot(d):
	edges = []
	t = d['type']
	for key in iter(d['edges']):
		for edge in d['edges'][key]:
			if t == 'digraph' and edges.count(key+' -> '+edge) < 1:
				edges.append(key+' -> '+edge)
			elif t == 'graph' and (edges.count(key+' -- '+edge) < 1 and edges.count(edge+' -- '+key) < 1):
				edges.append(key+' -- '+edge)
	return [''+d['type']+' '+d['name']+' {']+edges+['}']

def loadDot(filename,graphname):
	graphs = []
	for line in open(filename,'r'):
		pass

def renderDot(d):
	for line in d:
		print line

if __name__ == "__main__":
	g = parseDot(c)
	print g