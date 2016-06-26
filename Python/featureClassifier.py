from random import choice
from numpy import array, dot, random, argmax
import os

"""
TODO: Interface for manual labeling of images/json
	JSON labeling interface can be CLI
	image labeling should be canvas/pygame/tkinter?
		break image into chunks **square chunk priority**
		allow selection of chunks to label

training data format:
	(array([data]), label_index)
"""

unit_step = lambda x: 0 if x < 0 else 1
possLabels = []

#stopwords = []

def train(training_data):
	#w = array([0.0 for i in training_data[0][0]])
	w = random.random(len(training_data[0][0]))
	errors = []
	#eta = 0.5
	eta = 0.8
	n = 100
	for j in xrange(n):
		for i in xrange(len(training_data)):
			b = choice(training_data)
			x = b[0]
			expected = b[1]
			result = dot(w,x)
			#print expected,unit_step(result)
			#print expected,unit_step(result)
			error = expected-unit_step(result)
			#error = expected-argmax(result)
			errors.append(str(error))
			w += eta * error * x

	open('errors','w').write('\n'.join(errors))
	return w
	#for x, _ in training_data:
	#	result = dot(x,w)
	#	print("{}:{}->{}".format(x[:2],result,unit_step(result)))

def test(w,test_data):
	out = []
	#count = [0,0]
	for item in test_data:
		x = item[0]
		#l = item[1]
		#count[l] += 1
		r = dot(x,w)
		out.append(r)
		#out.append("{}:{}->{}".format(possLabels[l],r,unit_step(r)))
	#print count
	#open('textClassifier_out','w').write('\n'.join(out))
	return out

def bow_iter(string):
	if string.count(' ') > 1:
		return [item for item in string.split()]
	else:
		return [item for item in list(string)]

def bow(string,init):
	if len(init) == 0:
		fin = {}
	else:
		fin = dict(init)
	toggle = False
	if len(init) > 0:
		toggle = True
		for key in iter(init):
			fin[key] = 0
	for word in bow_iter(string):
		try:
			fin[word] += 1
		except KeyError:
			if not toggle:
				fin[word] = 1
	end = []
	for key in fin:
		end.append(fin[key])
	return end

def load_dir(dir):
	a = {}
	for f in os.listdir(dir):
		if not os.path.isfile(os.path.join(dir,f)):
			a[f] = [];
	for key in iter(a):
		for line in [f for f in os.listdir(dir+'/'+key) if os.path.isfile(os.path.join(dir+'/'+key, f))]:
			if not '._' in line:
				a[key].append(dir+'/'+key+'/'+line)
	return a


def bagofwords(string,s):
	f = string
	b = bow(f,s)
	end = []
	for key in b:
		end.append(b[key])
	end.append(1)
	return array(end)

def genTest(d,limit):
	a = {
		"training": [],
		"training_labels": [],
		"test": [],
		"test_labels": []
	}
	for k in iter(d):
		possLabels.append(k)
		print k, len(d[k])
		for i in xrange(len(d[k])):
			if i < limit:
				a['training'].append(d[k][i])
				a['training_labels'].append(possLabels.index(k))
			else:
				a['test'].append(d[k][i])
				a['test_labels'].append(possLabels.index(k))

	print {
		"training": len(a['training']),
		"training_labels": len(a['training_labels']),
		"test": len(a['test']),
		"test_labels": [a['test_labels'].count(possLabels[0]),a['test_labels'].count(possLabels[1])],
		"possLabels": possLabels
	}
	return a

def genTrainingData(d):
	s = bow(open('/nfs/panopticon/1000.txt').read(),{})

	endTrain = []
	endTest = []
	for i in range(len(d['training'])):
		endTrain.append(
			(array(
				bagofwords(d['training'][i],s)
			),
			d['training_labels'][i]
		))
	for i in range(len(d['test'])):
		endTest.append(
			(array(
				bagofwords(d['test'][i],s)
			),
			d['test_labels'][i]
		))
	return [endTrain,endTest]
def main():
	g = genTest(load_dir('/nfs/panopticon/review_polarity/txt_sentoken'),600)
	t = genTrainingData(g)
	#open('training.txt','w').write('\n'.join(t[0]))
	weight = train(t[0])
	#test_data = array([1,0,1])
	open('weights.txt','w').write(str(weight))
	test(weight,t[1])

if __name__ == "__main__":	
	main()