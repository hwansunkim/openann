from openann import *
from numpy import *
from time import *

def openAnnfile(filename):
	f = open(filename, 'r')
	line = f.readline()
	input_vector = line.split()

	N = int(input_vector[0])
	D = int(input_vector[1])
	F = int(input_vector[2])

	lines = f.readlines()
	X = float64([i.strip().split() for i in lines[::2]])
	Y = float64([i.strip().split() for i in lines[1::2]])
	f.close()
	return N,D,F,X,Y

def diff(x, y):
	ret = True
	for i in range(len(x)):
		if(x[i] != y[i]):
			ret = False
			break;
	return ret

def compact(x,y):
	ret_x = [list(x[0])]
	ret_y = [y[0]]
	for i in range(1,len(x)):
		key = True
		for j in range(0,i):
			if diff(x[i],x[j]): 
				key = False
				break;
		if key:
			ret_x += [list(x[i])]
			ret_y += [y[i]]
	return array(ret_x), array(ret_y)

def autoNorm(dataSet):
	minVals = dataSet.min(0)
	maxVals = dataSet.max(0)

	ranges = maxVals - minVals
	for i in range(len(ranges)):
		if (ranges[i] == 0): ranges[i] = 1
	normDataSet = zeros(shape(dataSet))
	m = dataSet.shape[0]
	normDataSet = dataSet - tile(minVals, (m,1))
	normDataSet = normDataSet / tile(ranges, (m,1))

	return normDataSet, ranges, minVals

def saveAnnfile(filename, x, y):
	f = open(filename, 'w')
	data = "%d %d %d\n" % (x.shape[0], x.shape[1], y.shape[1])
	f.write(data)
	for i in range(len(x)):
		f.write(" ".join(str(s) for s in list(x[i])))
		f.write("\n")
		f.write(" ".join(str(s) for s in list(y[i])))
		f.write("\n")
	f.close()
