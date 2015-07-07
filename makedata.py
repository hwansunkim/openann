from dataset import *
from sys import *

env = {}
for k in argv[1:]:
	tmp = k.split("=")
	env.update({tmp[0]:tmp[1]})

n,d,f,x,y = openAnnfile(env['file'])

outfile = open((env['file'].split('/')[-1]).split('.')[0] + ".half", 'w')

for i in range(1,d,2):                                                                     
	x[::,i-1] = x[::, i-1] / (abs(x[::,i] - 0.185369383532)+1)

d=d/2
X = x[::,::2]

outfile.writelines("%d %d %d\n"%(n,d,f))

for i in range(n):
	outfile.writelines(list("%.13lf "%item for item in X[i]))
	outfile.writelines("\n%.13lf\n"%y[i])

outfile.close()

