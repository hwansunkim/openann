from sys import *
from openann import *
from numpy import *
from time import *
import matplotlib.pyplot as plt

env = {}
for k in argv[1:]:
	tmp = k.split("=")
	env.update({tmp[0]:tmp[1]})

f = open(env['file'], 'r')

line = f.readline()
input_vector = line.split()

N = int(input_vector[0])
D = int(input_vector[1])
F = int(input_vector[2])

lines = f.readlines()
X = float64([i.strip().split() for i in lines[::2]])
Y = float64([i.strip().split() for i in lines[1::2]])
f.close()

dataset = DataSet(X, Y)

net = Net()
net.load(env['network'])

err = 0.0
f = []
d = []
for n in range(N):
	f += [net.predict(X[n])[0][0]]
	d += [Y[n][0]]
	err = ((Y[n] - net.predict(X[n]))**2).mean()

#ROC curve data
sorted_data = sorted(zip(f,d), reverse=False)
nongravity = float(d.count(0.0))
gravity    = float(d.count(1.0))

print nongravity, gravity

sorted_d = []
sorted_f = []
for sf,sd in sorted_data:
    sorted_d += [sd]
    sorted_f += [sf]

roc_x = []
roc_y = []

tmp = sorted_f[0]
for i in range(0, N):
	if( i == 0 or tmp < sorted_f[i]):
		roc_x += [1.0 - float(sorted_d[0:i].count(0.0))/nongravity] #1-Specificity
		roc_y += [float(sorted_d[i:].count(1.0))/gravity]   # Sensitivity
		tmp = sorted_f[i]
# AUC calculating.
tmp = 0
for i in roc_y:
	tmp += i

auc = tmp/len(roc_y)
text =  "[AUC : %f ]" % auc

#wskim's graph

smin = array(sorted_f).min()
smax = array(sorted_f).max()
ranges = smax - smin
wskim_y = [0]
wskim_y2 = [0]
rank = 0
step = ranges / 100
start = smin + step
next_step = start
for i in range(0,N):
	while sorted_f[i] >= next_step:
		next_step = next_step + step
		rank = rank + 1
		wskim_y += [0]
		wskim_y2 += [0]

	if(sorted_d[i] == 0.0): 
		wskim_y[rank] = wskim_y[rank] + 1
	else: 
		wskim_y2[rank] = wskim_y2[rank] + 1

wskim_x = numpy.linspace(start, next_step - step, len(wskim_y))
# Guide line plot
g_x = numpy.linspace(0.0,1.0, 10000)
g_y = numpy.linspace(0.0,1.0, 10000)

plt.clf()
plt.subplot(2,1,1)
plt.grid(True)
index = arange(len(wskim_y))
plt.bar(index, wskim_y, 0.3, alpha=0.2, color='b', label='0')
plt.bar(index+0.3, wskim_y2, 0.3, alpha=0.2, color='r', label='1')
plt.legend()
plt.subplot(2,1,2)
plt.grid(True)
plt.plot(roc_x,roc_y, '-r', label="ROC curve")
plt.plot(g_x, g_y, '--b', label="Guideline")
plt.title(env['network'].split('.net')[0])
plt.xlabel('False Alarm Probability')
plt.ylabel('Efficiency')
plt.xlim(xmin=1e-4, xmax=1)
plt.xscale('log')
plt.text(1e-2, 0.2, text)
plt.legend()
#plt.savefig("eval%s(%.4f).png" % (env['network'].split('.net')[0], auc))
plt.show()

