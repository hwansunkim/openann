from sys import *
from dataset import *
import subprocess

env = {}
for k in argv[1:]:
        tmp = k.split("=")
        env.update({tmp[0]:tmp[1]})

net = subprocess.check_output (env['network'] , shell=True)
networks = net.strip().split('\n')

filelists = []
ls = ['-', '--', '.-']
for i in networks:
	filelists += ["959126400_full_data_signif_over_dt/ALL_S6_959126400_full_set_%s_evaluation.ann" % (i.split('/')[-1].split('_')[5])]

g_x = linspace(0.0,1.0, 10000)
g_y = linspace(0.0,1.0, 10000)

plt.close('all')
p, (ax1) = plt.subplots(1)
ax1.grid(True)
ax1.plot(g_x, g_y, '--b', label="Guideline")
ax1.set_xscale('log')
for i in range(len(filelists)):
	N,D,F,X,Y = openAnnfile(filelists[i])
	dataset = DataSet(X, Y)
	net = Net()
	net.load(networks[i])
	f = []
	d = []
	roc_x = []
	roc_y = []
	err = 0.0
	auc = 0.0
	for n in range(N):
		f += [net.predict(X[n])[0][0]]
		d += [Y[n][0]]
		err += (Y[n] - net.predict(X[n]))**2

	roc_x, roc_y, auc = roc(f,d)
	ax1.plot(roc_x, roc_y, ls[i/7], linewidth=2, label="%s(%f)"%(networks[i],auc))

plt.legend(loc=0, prop={'size':7})
plt.show()

