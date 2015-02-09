try:
	from openann import *
except:
	print("OpenANN Python bindings are not installed!")
	exit(1)

try:
	from numpy import *
except:
	print("numpy is not installed!")
	exit(1)

try: 
	from matplotlib import pyplot as plt
except:
	print("matplotlib in not installed!")
	exit(1)

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

def drawROC(filename, f, d):
	sorted_data = sorted(zip(f,d), reverse=False)
	numOfTrue = float(d.count(1))
	numOfFalse = float(d.count(0))

	print "True(%d), False(%d)\n" %(numOfTrue, numOfFalse)
	sorted_f = array(sorted_data)[:,0]	
	sorted_d = array(sorted_data)[:,1]

	roc_x = []
	roc_y = []
	tmp = sorted_f[0]
	for i in range(len(sorted_f)):
		roc_x += [1.0 - float(list(sorted_d[0:i]).count(0.0)) / numOfFalse] # 1 - Specificity
		roc_y += [float(list(sorted_d[i:]).count(1.0)) / numOfTrue]   # Sensitivity	
		tmp = sorted_f[i]

	#AUC calculating
	tmp = 0
	for i in roc_y:
		tmp += i

	smin = sorted_f.min()
	smax = sorted_f.max()
	ranges = smax - smin

	trueCount = [0]
	falseCount = [0]
	rank = 0
	step = ranges / 100
	next_step = smin + step
	start = next_step	
	for i in range(len(sorted_f)):
		while sorted_f[i] >= next_step:
			next_step = next_step + step
			rank = rank + 1 
			trueCount += [0] 
			falseCount += [0] 

		if(sorted_d[i] == 0.0): 
			falseCount[rank] = falseCount[rank] + 1 
		else: 
			trueCount[rank] = trueCount[rank] + 1 

	ranks = numpy.linspace(start, next_step - step, len(trueCount))
	auc = tmp/len(roc_y)
	text = "[AUC :%f]" % (auc)
	
	# Guide line plot
	g_x = linspace(0.0,1.0, 10000)
	g_y = linspace(0.0,1.0, 10000)

	plt.close('all')
	f, (ax1, ax2) = plt.subplots(2)
	ax1.grid(True)
	ax1.set_title('Distribution')
	ax2.set_xlabel('Ranks')
	ax2.set_ylabel('Number of element')
	ax1.bar(ranks, falseCount, width=step/3, alpha=0.2, color='r', align='center', label='False')
	ax1.bar(ranks+step/3, trueCount, width=step/3, alpha=0.2, color='b', align='center', label='True')
	ax1.legend()
	ax2.grid(True)
	ax2.plot(roc_x,roc_y, '-r', label="ROC curve")
	ax2.plot(g_x, g_y, '--b', label="Guideline")
	ax2.set_title('RoC Curve')
	ax2.set_xlabel('False Alarm Probability')
	ax2.set_ylabel('Efficiency')
	ax2.set_xlim(xmin=1e-4, xmax=1)
	ax2.set_xscale('log')
	ax2.text(1e-2, 0.2, text)
	plt.legend(loc=0)
#	plt.savefig("%s($.4f).png"%(filename, auc))
	plt.savefig("log%s(%f).png"%(filename, auc))
#	plt.show()


