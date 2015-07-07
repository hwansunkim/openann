from sys import *
from dataset import *
import subprocess

env = {}
for k in argv[1:]:
        tmp = k.split("=")
        env.update({tmp[0]:tmp[1]})

net = subprocess.check_output (env['network'] , shell=True)
networks = net.strip().split('\n')
N,D,F,X,Y = openAnnfile(env['file'])

#for i in range(1,D,2):
#        X[::,i] = abs(X[::,i] - 0.185369383532)

#for i in range(1,D,2):
#        x[::,i-1] = x[::, i-1] / (abs(x[::,i] - 0.185369383532)+1)

#X = x[::,::2]

dataset = DataSet(X, Y)

g_x = linspace(0.0,1.0, 10000)
g_y = linspace(0.0,1.0, 10000)

plt.close('all')
p, (ax1) = plt.subplots(1)
ax1.grid(True)
ax1.plot(g_x, g_y, '--b', label="Guideline")
ax1.set_xscale('log')
for net_name in networks:
	net = Net()
	net.load(net_name)
	err = 0.0
	f = []
 	d = []
	roc_x = []
	roc_y = []
	auc = 0.0
	for n in range(N):
		f += [net.predict(X[n])[0][0]]
		d += [Y[n][0]]
		err += (Y[n] - net.predict(X[n]))**2

	print "MSE: %lf" % (err[0][0]/N)
	roc_x, roc_y, auc = roc(f,d)
	ax1.plot(roc_x, roc_y, '-', linewidth=2, label=net_name)

plt.legend(loc=0, prop={'size':7})
plt.show()

