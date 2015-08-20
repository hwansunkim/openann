from dataset import *
from sys import *

fd = open(argv[1], 'r')
pngfile = argv[1].split(".")

lines = fd.readlines()
a = float64([i.strip().split() for i in lines])

d = []
f = []
for b1,b2 in a:
	f += [b1]
	d += [b2]


x,a,b,fap = roc(f,d)

print fap
#print "FAP 0.1%% =  %2.1f%%"%(fap*100)
exit()
for i in range(len(x)):
	if x[i] <= 0.001:
		print  'FAP 0.1 %g'%((y[i-1] - y[i])/(x[i-1] - x[i])*(0.001 - x[i-1]) + y[i])
		break
