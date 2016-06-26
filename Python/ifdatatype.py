import couchdb,re
import string
from featureClassifier import train,test,bow
from numpy import array
couchdb = couchdb.Server()

def dictionary():
	f = open('/nfs/panopticon/1000.txt')
	a = string.letters
	d = string.digits
	p = string.punctuation
	l = list(a)+list(d)+list(p)
	for line in f:
		l.append(line.strip())

	e = {}
	for item in l:
		e[item] = 0
	return e

def genTrainData(inp):
	f = inp
	e = {}
	for d in f:
		for k in iter(d):
			try:
				if e[d[k]]['right'].count(bow(k,dictionary())) == 0 and d[k] != 'date': 
					e[d[k]]['right'].append( ( array( bow( k,dictionary() ) ), 1 ) )
					for x in iter(d):
						if d[x] != d[k]:
							e[d[k]]['wrong'].append( ( array( bow( x,dictionary() ) ), 0 ) )
			except KeyError:
				if d[k] != 'date':
					w = []
					for x in iter(d):
						if d[x] != d[k]:
							w.append( ( array( bow( x,dictionary() ) ), 0 ) )
					e[d[k]] = {'right': [ ( array( bow(k,dictionary()) ), 1 )], 'wrong': w}

	return e

def spatialWeight(data):
	return train(data['spatial']['right']+data['spatial']['wrong'])
def imageWeight(data):
	return train(data['image']['right']+data['image']['wrong'])
def textWeight(data):
	return train(data['text']['right']+data['text']['wrong'])

def init(data):
	weights = []
	#weights.append(spatialWeight(data))
	weights.append(imageWeight(data))
	weights.append(textWeight(data))
	return weights

def average(a):
	step = lambda x: 0 if x < 0 else 1
	d = []
	dd = [[],[]]
	fin = 0
	for item in a:
		#print item
		d.append(step(item))
	for i in range(len(d)):
		if d[i] == 1:
			dd[1].append(a[i])
		else:
			dd[0].append(a[i])
	for item in dd[1]:
		fin += item
	return fin/len(d)

def check(weights,data):
	labels = ['image','text']
	r = 5
	end = []
	biggest = 0
	for w in weights:
		avg = test(w,[(data, 3) for i in range(r)])
		#big = average(avg)
		#print avg
		end.append(average(avg))
	for item in end:
		if item > biggest:
			biggest = item
	return labels[end.index(biggest)]

def handle(w,inp):
	return check(w,bow(inp,dictionary()))

def main():
	train_data = genTrainData('/nfs/panopticon/labels')
	weights = init(train_data)
	return weights
if __name__ == "__main__":
	g = main()
	while True:
		print check(g,bow(raw_input("> "),dictionary()))
	#open('testOut','w').write(str(g))
