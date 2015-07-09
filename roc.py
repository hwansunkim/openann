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

drawROC(pngfile,f,d)
